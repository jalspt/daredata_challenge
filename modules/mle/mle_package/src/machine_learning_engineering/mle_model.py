from typing import Iterable, Any
import pandas as pd
from os.path import expanduser
import logging  # Add logging module

# Configure logging
logging.basicConfig(
	level=logging.INFO,
	format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


class MLEModel():
	# Add logger as a class attribute
	logger = logging.getLogger('MLEModel')

	def load(self, *args, **kwargs) -> Any:
		"""
		Loads the model and any required artifacts.
		To be implemented by the data scientist.
		"""
		self.logger.info(f"Loading model with args: {args}, kwargs: {kwargs}")
		raise NotImplementedError()

	def save(self, *args, **kwargs) -> None:
		"""
		Saves the model and any required artifacts to a given location.
		To be implemented by the data scientist.
		"""
		self.logger.info(f"Saving model with args: {args}, kwargs: {kwargs}")
		raise NotImplementedError()

	def fit(self, data: Any):
		"""Fits the model to the data. To be implemented by the data scientist.
		"""
		self.logger.info(f"Fitting model with data shape: {getattr(data, 'shape', 'unknown')}")
		raise NotImplementedError()

	def predict(self, features: Any) -> int:
		"""Predicts the label of unseen data. To be implemented by the data scientist.
		"""
		self.logger.info(f"Predicting with features shape: {getattr(features, 'shape', 'unknown')}")
		raise NotImplementedError()

	def predict_with_logging(self, client_idx: int, features: Any) -> None:
		"""
		Calls the predict function, implemented by the data scientist, and logs the results
		of the prediction to storage.
		"""
		self.logger.info(f"Predicting with logging for client: {client_idx}")
		predicted_label = self.predict(features)
		self.log_to_storage(client_idx, predicted_label)
		self.logger.info(f"Predicted label {predicted_label} for client {client_idx}")

		return predicted_label

	def log_to_storage(self, client_idx: int, predicted_label: int):
		"""
		Logs the prediction to the predictions table, on the database.
		Our extremely advanced "storage" is a text file on the `~/mle_storage` directory :-) 
		"""
		self.logger.info(f"Logging prediction to storage: client {client_idx}, label {predicted_label}")
		try:
			with open(f'{expanduser("~")}/mle_storage/labels', 'a+') as f:
				f.write(f"{client_idx},{predicted_label}\n")
			self.logger.info("Successfully logged prediction to storage")
		except FileNotFoundError:
			error_msg = "Have you created the ~/mle_storage directory?"
			self.logger.error(error_msg)
			print(error_msg)
