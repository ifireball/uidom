from typing import TypeVar, Generic

# Define a TypeVar used to parameterize the descriptor, linking the descriptor 
# to the attribute's type hint for strict type checking.
AttrT = TypeVar('AttrT')

class Sparse(Generic[AttrT]):
    """
    A generic descriptor that enforces attribute sparsity.

    Attributes are only stored on the instance if the value assigned differs 
    from the class-level default. This maintains memory efficiency for instances 
    that use the default value.

    This implementation is compatible with dataclasses, supports subclassing, 
    and works correctly with frozen dataclasses.
    
    NOTE ON SUBCLASSING: When overriding a default in a subclass, the descriptor 
    must be re-instantiated (e.g., `timeout: int = Sparse(default=10)`). 
    A raw assignment (e.g., `timeout: int = 10`) would mask the descriptor 
    and break the sparsity check during instance initialization.

    Examples demonstrating desired behavior:
    
    1. Base Class Sparsity (Instance uses default)

    >>> from dataclasses import dataclass, field
    >>> @dataclass
    ... class BaseConfig:
    ...     # Field 1: Overridden in SubConfig (to test default override)
    ...     timeout: int = Sparse(default=5) 
    ...     # Field 2: NOT overridden in SubConfig (to test inheritance sparsity)
    ...     retries: int = Sparse(default=2)
    ...     # A standard instance field
    ...     user_id: int = field(default=999)
    >>> base_a = BaseConfig()
    >>> base_a.timeout
    5
    >>> 'timeout' in base_a.__dict__
    False
    
    2. Base Class Override (Value stored on instance)
    
    >>> base_b = BaseConfig(timeout=15)
    >>> base_b.timeout
    15
    >>> 'timeout' in base_b.__dict__
    True
    
    3. Subclass Sparsity (Uses SubClass's new default)
    
    >>> @dataclass
    ... class SubConfig(BaseConfig):
    ...     # CORRECT PATTERN: Re-instantiating Sparse ensures __set__ is called.
    ...     timeout: int = Sparse(default=10) 
    >>> sub_c = SubConfig()
    >>> sub_c.timeout
    10
    >>> 'timeout' in sub_c.__dict__
    False
    
    4. Subclass Explicit Set to New Default (Should remain sparse)
    
    >>> sub_d = SubConfig(timeout=10)
    >>> sub_d.timeout
    10
    >>> 'timeout' in sub_d.__dict__
    False
    
    5. Subclass Non-Overridden Field Sparsity
    
    >>> sub_e = SubConfig()
    >>> sub_e.retries
    2
    >>> 'retries' in sub_e.__dict__
    False
    >>> 'retries' in SubConfig.__dict__
    False
    >>> 'timeout' in sub_e.__dict__
    False
    >>> 'timeout' in SubConfig.__dict__
    True

    6. Frozen Class Sparsity (Instance uses default)
    
    >>> @dataclass(frozen=True)
    ... class FrozenConfig:
    ...     # Field to test sparse initialization with frozen=True
    ...     threshold: float = Sparse(default=0.5)
    ...     # A standard instance field
    ...     name: str = "Test"
    >>> frozen_a = FrozenConfig()
    >>> frozen_a.threshold
    0.5
    >>> 'threshold' in frozen_a.__dict__
    False

    7. Frozen Class Explicit Override (Value stored on instance)

    >>> frozen_b = FrozenConfig(threshold=0.9)
    >>> frozen_b.threshold
    0.9
    >>> 'threshold' in frozen_b.__dict__
    True

    8. Frozen Class Mutation Attempt (Must fail after init)
    
    >>> try:
    ...     frozen_a.threshold = 1.0
    ... except AttributeError as e:
    ...     print("Error: " + str(e))
    Error: cannot assign to field 'threshold'
    
    9. Frozen Subclass Sparsity (Uses SubClass's overridden default)
    
    >>> @dataclass(frozen=True)
    ... class FrozenSubConfig(FrozenConfig):
    ...     # CORRECT PATTERN: Re-instantiating Sparse for a frozen subclass override.
    ...     threshold: float = Sparse(default=0.9) 
    >>> frozen_sub_c = FrozenSubConfig()
    >>> frozen_sub_c.threshold
    0.9
    >>> 'threshold' in frozen_sub_c.__dict__
    False

    10. Frozen Subclass Explicit Set to New Default (Should remain sparse)
    
    >>> frozen_sub_d = FrozenSubConfig(threshold=0.9)
    >>> frozen_sub_d.threshold
    0.9
    >>> 'threshold' in frozen_sub_d.__dict__
    False
    """

    def __init__(self, default: AttrT) -> None:
        """Initializes the descriptor with the default value."""
        self.initial_default: AttrT = default
        self.name = ""
    
    def __set_name__(self, owner: type[object], name: str) -> None:
        """
        Called automatically by Python to assign the attribute name.
        """
        self.name = name

    def __get__(self, instance: object|None, owner: type[object]) -> AttrT:
        """
        Retrieves the attribute value. Checks the instance first, then falls 
        back to the descriptor's initial default value.
        """
        if instance is None:
            # Class access: returns the default of THIS specific descriptor instance.
            return self.initial_default

        try:
            # 1. Attempt to get the value from the instance's private storage.
            return instance.__dict__[self.name]
        except (KeyError, AttributeError):
            # 2. If not found on the instance, return the default of THIS 
            # descriptor instance. The MRO check by the interpreter guarantees 
            # this is the correct effective default.
            return self.initial_default

    def __set__(self, instance: object, value: AttrT) -> None:
        """
        Sets the attribute value. Only stores the value on the instance if 
        it differs from the class's current default, ensuring sparsity.
        """        
        # If the value being set is equal to the class's current default
        if value == self.initial_default:
            # Check if it was previously set (non-default) and remove it 
            # to make the instance sparse again.
            if self.name in instance.__dict__:
                del instance.__dict__[self.name]
        else:
            # Value is different from the default, so we must store it 
            # explicitly on the instance.
            instance.__dict__[self.name] = value
