import os
import random

from PIL import Image
import numpy as np

import folder_paths

class SaveImageWebp:
	def __init__(self):
		self.output_dir = folder_paths.get_output_directory()
		self.type = "output"
		self.prefix_append = ""

	@classmethod
	def INPUT_TYPES(s):
		return {
			"required": {
				"images": ("IMAGE", {"tooltip": "The images to save."}),
				"filename_prefix": ("STRING", {"default": "ComfyUI", "tooltip": "The prefix for the file to save. This may include formatting information such as %date:yyyy-MM-dd% or %Empty Latent Image.width% to include values from nodes."})
			},
		}

	RETURN_TYPES = ()
	FUNCTION = "save_images"

	OUTPUT_NODE = True

	CATEGORY = "image"
	DESCRIPTION = "Saves the input images to your ComfyUI output directory."

	def save_images(self, images, filename_prefix="ComfyUI", prompt=None, extra_pnginfo=None):
		filename_prefix += self.prefix_append
		full_output_folder, filename, counter, subfolder, filename_prefix = folder_paths.get_save_image_path(filename_prefix, self.output_dir, images[0].shape[1], images[0].shape[0])
		results = list()
		for (batch_number, image) in enumerate(images):
			i = 255. * image.cpu().numpy()
			img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))

			filename_with_batch_num = filename.replace("%batch_num%", str(batch_number))
			file = f"{filename_with_batch_num}_{counter:05}_.webp"
			img.save(os.path.join(full_output_folder, file), lossless=True, quality=100)
			results.append({
				"filename": file,
				"subfolder": subfolder,
				"type": self.type
			})
			counter += 1

		return { "ui": { "images": results } }

class PreviewImageWebp(SaveImageWebp):
	def __init__(self):
		self.output_dir = folder_paths.get_temp_directory()
		self.type = "temp"
		self.prefix_append = "_temp_" + ''.join(random.choice("abcdefghijklmnopqrstupvxyz") for x in range(5))

	@classmethod
	def INPUT_TYPES(s):
		return {
			"required":	{
				"images": ("IMAGE", ),
			},
		}