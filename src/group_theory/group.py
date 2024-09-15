class Group:
    """ Represents a group. """

    def __init__(self, element_values, operation, identity_value=None) -> None:
        self.element_values = element_values
        self._operation = operation
        self._identity_value = identity_value

    def __eq__(self, other):
        if not isinstance(other, Group):
            return NotImplemented
        
        # Compare element_values and identity_value
        if set(self.element_values) != set(other.element_values) or self._identity_value != other._identity_value:
            return False
        
        # Compare operations by applying them to all pairs of elements
        for a in self.element_values:
            for b in self.element_values:
                if self._operation(a, b) != other._operation(a, b):
                    return False
        
        return True

    def elements(self):
        return [GroupElement(element, self) for element in self.element_values]

    def operation(self, a, b):
        return self._operation(a, b)

    def identity(self):
        if self._identity_value is None:
            # Find identity if not provided
            for e in self.element_values:
                if all(self.operation(e, x) == x and self.operation(x, e) == x for x in self.element_values):
                    self._identity_value = e
                    break
        return GroupElement(self._identity_value, self)

    def inverse(self, a):
        for x in self.element_values:
            if self.operation(a, x) == self.identity().element and self.operation(x, a) == self.identity().element:
                return GroupElement(x, self)
        raise ValueError(f"Inverse not found for {a}")

    def order(self):
        return len(self.element_values)

    def is_abelian(self):
        return all(self.operation(a, b) == self.operation(b, a) 
                for a in self.element_values 
                for b in self.element_values)
    

    @classmethod
    def direct_product(cls, *groups):
        """
        Construct the direct product of given groups.
        """
        def cartesian_product(*iterables):
            if not iterables:
                yield ()
            else:
                for item in iterables[0]:
                    for rest in cartesian_product(*iterables[1:]):
                        yield (item,) + rest

        element_values = list(cartesian_product(*(group.element_values for group in groups)))
        
        def operation(a, b):
            return tuple(group._operation(a[i], b[i]) for i, group in enumerate(groups))
        
        identity_value = tuple(group.identity().element for group in groups)
        
        return cls(element_values, operation, identity_value)


    @classmethod
    def semidirect_product(cls, N, H, action):
        """
        Construct the semidirect product of groups N and H.
        action: function(h, n) -> n that defines how H acts on N
        """
        elements = [(n, h) for n in N.element_values for h in H.element_values]
        
        def operation(a, b):
            (n1, h1), (n2, h2) = a, b
            return (N.operation(n1, action(h1, n2)), H.operation(h1, h2))
        
        return cls(elements, operation)


class NamedGroup(Group):
    def __init__(self, element_values, operation, identity_value=None, name=None):
        super().__init__(element_values, operation, identity_value)
        self.name = name

    @classmethod
    def direct_product(cls, *groups):
        result = super().direct_product(*groups)
        name = " × ".join(getattr(group, 'name', f"Group{i}") for i, group in enumerate(groups))
        return cls(result.element_values, result._operation, result._identity_value, name)    


class GroupElement:
    """ A class to represent an element of a group. """

    def __init__(self, element, group: Group) -> None:
        self.element = element
        self.group = group

    def __mul__(self, other):
        return GroupElement(self.group.operation(self.element, other.element), self.group)

    def __pow__(self, n):
        if n == 0:
            return self.group.identity()
        elif n > 0:
            result = self
            for _ in range(n - 1):
                result *= self
            return result
        else:
            return self.inverse() ** (-n)

    def __eq__(self, other):
        return self.element == other.element and self.group == other.group

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return str(self.element)

    def __repr__(self):
        return f"GroupElement({self.element}, {self.group})"

    def inverse(self):
        return self.group.inverse(self.element)

    def order(self):
        power = self
        order = 1
        while power != self.group.identity():
            power *= self
            order += 1
        return order
