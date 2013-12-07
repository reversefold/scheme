from scheme.environment import environment
from scheme.parser.token import base

class let_t(base.token):
    symbol = 'let'

    @staticmethod
    def eval(env, var_list, *exprs):
        subenv = environment(env)
        for name, init in var_list:
            # TODO: assumption here that name is a label
            subenv[name.value] = init.eval(env)
        return [expr.eval(subenv) for expr in exprs][-1]

    @staticmethod
    def _ceval_env(k, env, var_list):
        def with_val(v):
            #TODO: assumption that name is a label
#            print "let %s = %r" % (var_list[0][0].value, v)
            env[var_list[0][0].value] = v
            if len(var_list) == 1:
                return base.Bounce(k)
            return base.Bounce(let_t._ceval_env, k, env, var_list[1:])
        return base.Bounce(var_list[0][1].ceval, with_val, env)

    _cache = {}

    @staticmethod
    def ceval(k, env, var_list, *exprs):
        subenv = environment(env)
        def with_env():
#            def with_flattened_env(flat):
                # TODO: only want the values in var_list, not env()
                #   Actually, only want those values that will be used in the lambda....but the var_list should work for now
                #    Not sure if the outer scope applies the same to lambdas in the spec
#                key = str(base.tuple([base.tuple([base.tuple([name, value]) for name, value in flat.items()]), base.tuple(exprs)]))
#                print "(\n %s\n)\n%s" % ("\n ".join(
#                    [str(base.tuple([name, value])) for name, value in flat.items()]), base.tuple(exprs))
                key = "(\n %s\n)\n%s" % (
                    "\n ".join(
                        [str(base.tuple([name, subenv[name.value]])) for name, expr in var_list]),
                    base.tuple(exprs))
                #print key
                if key in let_t._cache:
#                    print "cache win for:\n%s" % (key,)
                    #print "cached value %s for %s" % (let_t._cache[key], key)
                    return base.Bounce(k, let_t._cache[key])
                def with_value(v):
                    let_t._cache[key] = v
                    return base.Bounce(k, v)
                return base.Bounce(base.return_last, with_value, subenv, exprs)
#            return base.Bounce(subenv.cflattened, with_flattened_env)
        return base.Bounce(let_t._ceval_env, with_env, subenv, var_list)

class lambda_t(base.token):
    symbol = 'lambda'

    @staticmethod
    def eval(env, arg_labels, *exprs):
        return lambda_i(env, arg_labels, exprs)

    @staticmethod
    def ceval(k, env, arg_labels, *exprs):
        return base.Bounce(k, lambda_i(env, arg_labels, exprs))

class lambda_i(base.token):
    def __init__(self, env, arg_labels, exprs, name=None):
        self.arg_labels = arg_labels
        self.exprs = exprs
        self.name = name

    def eval(self, env, *arg_values):
        if len(self.arg_labels) != len(arg_values):
            raise Exception("number of labels (%r, %s) and values (%r, %s) does not match when calling %s"
                            % (len(self.arg_labels),
                               self.arg_labels,
                               len(arg_values),
                               arg_values, self))
        return let_t.eval(
            env,
            base.tuple(
                [base.tuple([self.arg_labels[i], arg_values[i]])
                 for i in xrange(len(self.arg_labels))]),
            *self.exprs)

    def ceval(self, k, env, *arg_values):
        if len(self.arg_labels) != len(arg_values):
            raise Exception("number of labels (%r, %s) and values (%r, %s) does not match when calling %s"
                            % (len(self.arg_labels),
                               self.arg_labels,
                               len(arg_values),
                               arg_values, self))
        return base.Bounce(let_t.ceval, k,
            env,
            base.tuple(
                [base.tuple([self.arg_labels[i], arg_values[i]])
                 for i in xrange(len(self.arg_labels))]),
            *self.exprs)

    def __str__(self):
        return '(lambda %s %s %s)' % (
            self.name if self.name is not None else '<unnamed>',
            self.arg_labels, base.tuple(self.exprs))

class named_lambda_t(base.token):
    symbol = 'named-lambda'

    @staticmethod
    def eval(env, arg_labels, *exprs):
        return lambda_i(env, arg_labels[1:], exprs, name=arg_labels[0])

    @staticmethod
    def ceval(k, env, arg_labels, *exprs):
        return base.Bounce(k, lambda_i(env, arg_labels[1:], exprs, name=arg_labels[0]))
