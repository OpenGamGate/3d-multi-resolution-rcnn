from .base_assigner import BaseAssigner
from .max_iou_assigner import MaxIoUAssigner
from .max_iou_assigner_parcel import MaxIoUAssignerParcel
from .assign_result import AssignResult

__all__ = ['BaseAssigner', 'MaxIoUAssigner', 'AssignResult', 'MaxIoUAssignerParcel']
