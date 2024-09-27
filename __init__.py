from .nodes import SaveImageWebp
from .nodes import PreviewImageWebp

NODE_CLASS_MAPPINGS = {
	"SaveImageWebp" : SaveImageWebp,
	"PreviewImageWebp": PreviewImageWebp,
}

__all__ = ['NODE_CLASS_MAPPINGS']
