from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
# from scipy import special as sp


def _to_tensor(x, dtype):
    return np.asarray(x, dtype=dtype)


def astensor(tensor, dtype):
    return np.array(tensor, dtype=dtype)


def aslist(tensor):
    tensor = astensor(tensor)
    return tensor.tolist()


def outer(x, y):
    x = astensor(x)
    y = astensor(y)
    return np.outer(x, y)


def sum(tensor, axis=None):
    tensor = self.astensor(tensor)
    return np.sum(tensor, axis=axis)

def product(self, tensor, axis=None):
    tensor = self.astensor(tensor)
    return np.product(tensor, axis = axis)

def ones(self, shape):
    return np.ones(shape)

def power(self,x, y):
    x = self.astensor(x)
    y = self.astensor(y)
    return np.power(x, y)

def sqrt(self,tensor):
    tensor = self.astensor(tensor)
    return np.sqrt(tensor)

    def divide(self,x, y):
        x = self.astensor(x)
        y = self.astensor(y)
        return np.divide(x, y, out=np.zeros_like(x), where=y!=0)

    def log(self,tensor):
        tensor = self.astensor(tensor)
        return np.log(tensor)

    def exp(self,tensor):
        tensor = self.astensor(tensor)
        return np.exp(tensor)

    def stack(self, sequence, axis = 0):
        return np.stack(sequence, axis = axis)

    def where(self, condition, x, y):
        condition = self.astensor(condition)
        x = self.astensor(x)
        y = self.astensor(y)
        return np.where(condition, x, y)

    def concatenate(self, sequence):
        return np.concatenate(sequence)

    def poisson(self, n, lam):
        n = np.asarray(n)
        if self.pois_from_norm:
            return self.normal(n,lam, self.sqrt(lam))
        return np.exp(n*np.log(lam)-lam-gammaln(n+1.))

    def normal(self, x, mu, sigma):
        return norm.pdf(x, loc=mu, scale=sigma)

class backend_tensorflow(object):
    def __init__(self, **kwargs):
        self.session = kwargs.get('session')

    def tolist(self,tensor_in):
        tensor_in = self.astensor(tensor_in)
        return self.session.run(tensor_in).tolist()

    def outer(self, tensor_in_1, tensor_in_2):
        tensor_in_1 = self.astensor(tensor_in_1)
        tensor_in_2 = self.astensor(tensor_in_2)
        tensor_in_1 = tensor_in_1 if tensor_in_1.dtype is not tf.bool else tf.cast(tensor_in_1, tf.float32)
        tensor_in_1 = tensor_in_1 if tensor_in_2.dtype is not tf.bool else tf.cast(tensor_in_2, tf.float32)
        return tf.einsum('i,j->ij', tensor_in_1, tensor_in_2)

    def astensor(self, tensor_in, dtype=tf.float32):
        if isinstance(tensor_in, tf.Tensor):
            v = tensor_in
        else:
            v = tf.convert_to_tensor(tensor_in)
        if v.dtype is not dtype:
            v = tf.cast(v, dtype)
        return v

    def sum(self, tensor_in, axis=None):
        tensor_in = self.astensor(tensor_in)
        return tf.reduce_sum(tensor_in) if (axis is None or tensor_in.shape == tf.TensorShape([])) else tf.reduce_sum(tensor_in, axis)

    def product(self, tensor_in, axis=None):
        tensor_in = self.astensor(tensor_in)
        return tf.reduce_prod(tensor_in) if axis is None else tf.reduce_prod(tensor_in, axis)

    def ones(self, shape):
        return tf.ones(shape)

    def power(self,tensor_in_1, tensor_in_2):
        tensor_in_1 = self.astensor(tensor_in_1)
        tensor_in_2 = self.astensor(tensor_in_2)
        return tf.pow(tensor_in_1, tensor_in_2)

    def sqrt(self,tensor_in):
        tensor_in = self.astensor(tensor_in)
        return tf.sqrt(tensor_in)

    def divide(self,tensor_in_1, tensor_in_2):
        tensor_in_1 = self.astensor(tensor_in_1)
        tensor_in_2 = self.astensor(tensor_in_2)
        return tf.divide(tensor_in_1, tensor_in_2)

    def log(self,tensor_in):
        tensor_in = self.astensor(tensor_in)
        return tf.log(tensor_in)

    def exp(self,tensor_in):
        tensor_in = self.astensor(tensor_in)
        return tf.exp(tensor_in)

    def stack(self, sequence, axis = 0):
        return tf.stack(sequence, axis = axis)

    def where(self, mask, tensor_in_1, tensor_in_2):
        mask = self.astensor(mask)
        tensor_in_1 = self.astensor(tensor_in_1)
        tensor_in_2 = self.astensor(tensor_in_2)
        return mask * tensor_in_1 + (1-mask) * tensor_in_2

    def concatenate(self, sequence):
        return tf.concat(sequence, axis=0)

    def simple_broadcast(self, *args):
        broadcast = []
        def generic_len(a):
            try:
                return len(a)
            except TypeError:
                if len(a.shape) < 1:
                    return 0
                else:
                    return a.shape[0]

        maxdim = max(map(generic_len,args))
        for a in args:
            broadcast.append(self.astensor(a) if generic_len(a) > 1 else a*self.ones(maxdim))
        return broadcast

    def poisson(self, n, lam):
        # could be changed to actual Poisson easily
        return self.normal(n,lam, self.sqrt(lam))

    def normal(self, x, mu, sigma):
        x = self.astensor(x)
        mu = self.astensor(mu)
        sigma = self.astensor(sigma)
        normal = tf.distributions.Normal(mu,sigma)
        return normal.prob(x)
