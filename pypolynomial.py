##############################################################################################
# Ring Class
##############################################################################################

class Ring:
    def __init__(self, add, sub, mult, contains, zero, real_subset = True, name = "", to_str = None):
        """
        Initialize a ring object. A ring is a set of elements equipped with two operators, + and *, and satisfying the ring axioms.
        The ring class implements adding and multiplying ring elements, along with a function that can tell you if an object is an element of the ring.

        arguments:
        -- add: A function that accepts two arguments: "a" and "b", and returns the value "a+b"
        -- sub: A function that accepts two arguments: "a" and "b", and returns the value "a-b". This is included as a way to define additive inverses.
        -- mult: A function that accepts two arguments: "a" and "b", and returns the value "a*b"
        -- contains: A function that accepts one argument: "a", and returns True if that object is an element of the ring, and false otherwise.
        -- zero: the additive identity in the ring.
        -- real_subset: a boolean indicating whether the ring is a subset of the real numbers.
        """
        self.contains = contains
        self.add = add
        self.sub = sub
        self.mult = mult
        self.zero = zero
        self.real_subset = real_subset
        self.name = name
        self.to_str = to_str

    def __equal__(self, other):
        if self.add == other.add and self.sub == other.sub and self.mult == other.mult and self.contains == other.contains and self.zero == other.zero and self.real_subset == other.real_subset:
              return True
        return False

##############################################################################################
# Field Class (Ring Subclass)
##############################################################################################

class Field(Ring):
    def __init__(self, add, sub, mult, contains, zero, identity, inverse, real_subset = True, name = "", to_str = None):
        """
        Initialize a ring object. A ring is a set of elements equipped with two operators, + and *, and satisfying the ring axioms.
        The ring class implements adding and multiplying ring elements, along with a function that can tell you if an object is an element of the ring.
    
        arguments:
        -- add: A function that accepts two arguments: "a" and "b", and returns the value "a+b"
        -- sub: A function that accepts two arguments: "a" and "b", and returns the value "a-b". This is included as a way to define additive inverses.
        -- mult: A function that accepts two arguments: "a" and "b", and returns the value "a*b"
        -- contains: A function that accepts one argument: "a", and returns True if that object is an element of the ring, and false otherwise.
        -- zero: The additive identity in the ring 0R
        -- identity: The multiplicative identity 1R.
        -- inverse: A function that accepts one argument: "a", and returns the multiplicative inverse, "a^-1".
        """
        super().__init__(add, sub, mult, contains, zero, real_subset, name = name, to_str = to_str)
        self.inv = inverse
        self.one = identity

##############################################################################################
# Premade Rings
##############################################################################################

# Predefined rings Z, Q, C
def add(a,b):
    return a+b
def sub(a,b):
    return a-b
def mult(a,b):
    return a*b
def inverse(a):
    return 1/a
def containsC(a):
    try:
        a-complex(1,1)
        return True
    except:
        return False
def containsZ(a):
    if type(a) == type(1):
        return True
    return False
def containsQ(a):
    try:
        float(a)
        return True
    except:
        return False

Z = Ring(add, sub, mult, containsZ, zero = 0, real_subset = True, name = "Z")
Q = Field(add, sub, mult, containsQ, 0, 1, inverse, real_subset = True, name = "Q")
C = Field(add, sub, mult, containsC, 0, 1, inverse, real_subset = False, name = "C")

# Polynomial Quotient Rings

def poly_quotient_ring(p):
    """
    returns a field of the form F[x]/p(x), where F is a field containing the coefficients of p(x).
    IMPORTANT: This function does NOT check if p(x) is irreducible in F[x]. It is up to the user to ensure that p(x) is irreducible.
    """
    if not p.over_field:
        raise Exception("Can only extend fields, but " + p.R.name+ " is not a field")
    
    def ext_add(f : Polynomial, g : Polynomial):
        """
        returns the remainer of f+g mod p.
        """
        _, r = (f+g)/p
        return r
    
    def ext_sub(f : Polynomial, g : Polynomial):
        """
        returns the remainer of f-g mod p.
        """
        _, r = (f-g)/p
        return r
    
    def ext_mult(f : Polynomial, g : Polynomial):
        """
        returns the remainer of f*g mod p.
        """
        _, r = (f*g)/p
        return r
    
    def ext_contains(f : Polynomial):
        """
        returns True if f is a polynomial over the same field as p. Returns False otherwise.
        """
        if type(f) is Polynomial and f.R == p.R:
            return True
        return False
    
    def ext_inv(f: Polynomial):
        """
        returns the multiplicative inverse of f in the field F[x]/p(x).
        """
        t = Polynomial(coeffs = {0:p.R.zero}, R = p.R)
        r = Polynomial(p.coeffs, p.R)
        newt = Polynomial({0:p.R.one}, R = p.R)
        newr = Polynomial(f.coeffs, p.R)
        while newr.degree() >= 0:
            q, _ = r/newr
            r, newr = newr, r-(q*newr)
            t, newt = newt, t-(q*newt)
        if r.degree() > 0:
            raise Exception("p is irreducible or a is a multiple of p")
        normalizer, _ = Polynomial({0:p.R.one}, p.R) / r
        return normalizer*t
    
    def ext_to_str(f: Polynomial):
        """
        returns a string representation of the equivalence class [f(x)]
        """
        return "[" + str(f) + "]"
        
    ext_zero = Polynomial({0:p.R.zero}, p.R)
    ext_one = Polynomial({0:p.R.one}, p.R)

    return Field(ext_add, 
                 ext_sub, 
                 ext_mult, 
                 ext_contains, 
                 ext_zero, 
                 ext_one, 
                 ext_inv, 
                 real_subset = False, 
                 name = p.R.name + "/(" + str(p) + ")", 
                 to_str = ext_to_str
                )

##############################################################################################
# Polynomial Class
##############################################################################################

class Polynomial:
    
    # Constructor
    
    def __init__(self, coeffs, R):
        """
        Initializes a Polynomial object.

        arguments:
        -- coeffs: A dictionary where every (key, value) pair corresponds to a power and its coefficient (e.g. {1:1, 2:1, 3:4} corresponds to "x + x^2 + 4x^3").
        -- R: a Ring instance.
        """
        self.R = R
        self.coeffs = {0:self.R.zero}
        # check that the coefficients are in the ring
        for n in coeffs.keys():
            a = coeffs[n]
            if R.contains(a):
                self.add_coeff(a, n)
            else:
                raise Exception("'" + str(a) + "' not an element of your ring.")
        self.over_field = True
        try:
            self.R.one # rings do not have the "R.one" attribute, but fields do
        except:
            self.over_field = False

    # Getters
    
    def get_coeff(self, n):
        """
        retrieves the coefficient of degree "n" from the polynomial. Returns zero if the coefficient dictionary does not contain "n"
        """
        if(n < 0):
            raise Exception("n must be >= 0. Detected n =", n)
        if n in self.coeffs.keys():
            return self.coeffs[n]
        else:
            return self.R.zero
    
    def degree(self):
        """
        returns the highest power with nonzero coefficient.
        NOTE we adopt the convention that the zero polynomial has degree "-1"
        """
        d = max(self.coeffs.keys())
        if self.get_coeff(d) == self.R.zero:
            return -1
        return d
        
    # Setters
    
    def add_coeff(self, a,n):
        """
        adds the value of a to the coefficient of degree n

        arguments:
        -- a: The coefficient to add to the polynomial.
        -- n: The degree to add "a" to.
        """
        if(n < 0):
            raise Exception("n must be >= 0. Detected n =", n)
        if n in self.coeffs.keys():
            self.coeffs[n] = self.R.add(self.coeffs[n], a)
        else:
            self.coeffs[n] = self.R.add(self.R.zero, a)
        if n != 0 and self.coeffs[n] == self.R.zero:
            self.coeffs.pop(n)

    # Display Functions

    def __str__(self):
        if len(self.coeffs) == 0:
            return "0"
        if len(self.coeffs) == 1 and self.get_coeff(0) == self.R.zero:
            return "0"
        # get the lowest degree with nonzero coefficient
        lowest_nonzero_deg = 0
        for n in range(0, self.degree() + 1):
            if self.get_coeff(n) != self.R.zero:
                lowest_nonzero_deg = n
                break
        s = ""
        for n in range(0, self.degree() + 1):
            a = self.get_coeff(n)
            if a != self.R.zero:
                # if we are working with real number coefficients, display the first  coefficient with a "-" if its negative
                if self.R.real_subset:
                    if n == lowest_nonzero_deg:
                        if self.get_coeff(n) < self.R.zero: # comparison allowed since the ring is a subset of R
                            s += "-"
                    if abs(a) != 1 or n == 0:
                        s += str(abs(a))
                # if we aren't in a real number subset print the first element with no sign
                else:
                    if self.R.to_str is not None:
                        s += self.R.to_str(a)
                    else:
                        s += str(a)
                if n > 0:
                    s += "x"
                if n > 1:
                    s += "^" + str(n)
                # if we are in a real number subset, test to see if we use a "-" for the next coefficient
                if self.R.real_subset:
                    a_next = self.R.zero
                    j = 1
                    while a_next == self.R.zero and n+j < self.degree() + 1:
                        a_next = self.get_coeff(n+j)
                        j += 1
                    if a_next < self.R.zero: # comparison allowed since the ring is a subset of R
                        s += " - "
                    else: s += " + "
                else:
                    s += " + "
        s = s[:-3] # remove the " + " we added at the end
        return s

    def __repr__(self):
        return "Polynomial(" + str(self) + ", R = " + self.R.name + ")"
        
    # Arithmetic
    
    def __add__(self, other):
        """
        Add two Polynomial objects and return a new Polynomial object.

        arguments:
        other - polynomial to be added.

        returns
        h - the polynomial equal to self + other
        """
        if self.R != other.R :
            raise Exception("Cannot add two polynomials over different rings.")
        h = Polynomial(coeffs = {0:self.R.zero}, R = self.R)
        for deg in self.coeffs.keys():
            h.add_coeff(self.coeffs[deg], deg)
        for deg in other.coeffs.keys():
            h.add_coeff(other.coeffs[deg], deg)
        return h
    
    def __mul__(self, other):
        """
        Multiply two Polynomial objects and return a new Polynomial object. Returns a new polynomial equal to the product of the two arguments.

        args:
        other - the polynomial to multiply by

        returns:
        h - the polynomial product
        """
        if(self.R != other.R):
            raise Exception("Cannot multiply two polynomials over different rings.")
        max_deg = self.degree() + other.degree()
        h = Polynomial(coeffs ={0:self.R.zero}, R = self.R)
        for i in range(0, max_deg+1):
            a = self.R.zero
            for k in range(0, i+1):
                a_self = self.R.zero
                a_other = self.R.zero
                if k in self.coeffs.keys():
                    a_self = self.coeffs[k]
                if i-k in other.coeffs.keys():
                    a_other = other.coeffs[i-k]
                a = self.R.add(a, self.R.mult(a_self,a_other))
            h.add_coeff(a, i)
        return h

    def __sub__(self, other):
        if self.R != other.R :
            raise Exception("Cannot add two polynomials over different rings.")
        h = Polynomial(coeffs = {0:self.R.zero}, R = self.R)
        for deg in self.coeffs.keys():
            h.add_coeff(self.coeffs[deg], deg)
        for deg in other.coeffs.keys():
            h.add_coeff(self.R.sub(self.R.zero, other.coeffs[deg]), deg)
        return h

    def __div__(self, divisor):
        """
        divide a polynomial by another. Returns the unique quotient and the remainder as specified by the division algorithm (theorem).
        Note the polynomials must have coefficients in a field for the theorem to hold.
        """
        return self.__divide(divisor)

    def __truediv__(self, divisor):
        """
        divide a polynomial by another. Returns the unique quotient and the remainder as specified by the division algorithm (theorem).
        Note the polynomials must have coefficients in a field for the theorem to hold.
        """
        return self.__divide(divisor)

    def __divide(self, g):
        f = Polynomial(coeffs = self.coeffs, R = self.R)
        if(f.R != g.R):
            raise Exception("Cannot divide two polynomials over different fields.")
        if not f.over_field:
            raise Exception("The division algorithm only holds in fields, but", self.R.name, "is not a field.")
        q = Polynomial(coeffs = {0:f.R.zero}, R = f.R)
        while g.degree() <= f.degree():
            a = f.coeffs[f.degree()]
            b = g.coeffs[g.degree()]
            b_inv = f.R.inv(b)
            c = f.R.mult(a, b_inv)
            n = f.degree() - g.degree()
            q.add_coeff(c, n)
            f = f - (g * Polynomial(coeffs = {n : c}, R = f.R))
        return q, f

    def __call__(self, x):
        """
        Evaluate the polynomial at a given value of x.
        """
        result = self.R.zero
        for deg in self.coeffs.keys():
            if deg > 0:
                a = x
                if deg > 1:
                    for i in range(1,deg):
                        a = self.R.mult(a,x)
                result = self.R.add(result, self.R.mult(a,self.get_coeff(deg)))
            else:
                result = self.R.add(result, self.get_coeff(deg))
        return result
    
    # Logic

    def __eq__(self, other):
        if self.R != other.R:
            return False
        if self.degree() != other.degree():
            return False
        for n in range(0, self.degree() + 1):
            if self.get_coeff(n) != other.get_coeff(n):
                return False
        return True

##############################################################################################
# Functions on Polynomials
##############################################################################################

def gcd(f : Polynomial, g : Polynomial):
    """
    returns the greatest common divisor of f and g polynomials. Note to guarantee that the gcd exists, we require that f and g be polynomials with coefficients in a field.
    """
    a = Polynomial(f.coeffs, f.R)
    b = Polynomial(g.coeffs, g.R)
    if(f.R != g.R):
        raise Exception("Cannot take the GCD of two polynomials over different rings.")
    if not f.over_field:
        raise Exception("the GCD is not guaranteed to exist if R is not a field")
    while b.degree() >= 0:
        _, r = a/b
        a = Polynomial(b.coeffs, b.R)
        b = Polynomial(r.coeffs, r.R)
    monic_rescaler = a.R.inv(a.get_coeff(a.degree()))
    a = Polynomial({0:monic_rescaler}, R = a.R) * a
    return a


