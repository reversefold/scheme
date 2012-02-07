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

    @staticmethod
    def ceval(k, env, var_list, *exprs):
        subenv = environment(env)
        def with_env():
            return base.Bounce(base.return_last, k, subenv, exprs)
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
        return let_t().eval(
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
        return base.Bounce(let_t().ceval, k,
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
