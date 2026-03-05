class VacuumException(Exception):
    pass


class ContainerFullException(VacuumException):
    pass


class FilterDegradedException(VacuumException):
    pass


class MotorStateError(VacuumException):
    pass
