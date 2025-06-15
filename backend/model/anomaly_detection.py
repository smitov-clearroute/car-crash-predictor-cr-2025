from typing import Any, Optional
import pandas as pd
import numpy as np

class AnomalyDetection:
    """
    A class for detecting anomalies in a dataset using z-scores.

    Attributes:
        _threshold (int): The threshold for determining anomalies.
        _train_data_file (str): The path to the training data CSV file.
        df (pd.DataFrame): The DataFrame containing the training data.
        mean_std (pd.DataFrame): A DataFrame containing the mean and standard deviation of each column.
    """

    def __init__(self, train_data_file: str, threshold: int = 3):
        """
        Initializes the AnomalyDetection class with a threshold and training data file.

        :param train_data_file: The path to the training data CSV file.
        :param threshold: The threshold for determining anomalies.
        """
        self._train_data_file = train_data_file
        self._threshold = threshold
        self.df = self.__get_df_from_csv()
        self.mean_std = self.__get_mean_std_data()

    def calculate_anomaly_score(self, column: str, value: float) -> float:
        """
        Calculates the anomaly score for a given value in a specified column.

        The anomaly score is calculated based on the z-score of the value relative to the mean and standard deviation
        of the specified column.

        :param column: The name of the column for which to calculate the anomaly score.
        :param value: The value to evaluate for anomaly detection.
        :return: A float representing the anomaly score, normalized between 0 and 1.
        """
        z_score = (value - self.mean_std.loc[column, 'mean']) / self.mean_std.loc[column, 'std']
        anomaly_score = (z_score + self.threshold) / 6

        return np.clip(anomaly_score, 0, 1)

    def __get_df_from_csv(self) -> Optional[pd.DataFrame]:
        """
        Reads the training data from a CSV file and returns it as a DataFrame.

        :return: A pandas DataFrame containing the training data, or None if an error occurs.
        """
        try:
            return pd.read_csv(self.train_data_file)
        except FileNotFoundError:
            print('Error: The file \'{}\' was not found.'.format(self.train_data_file))
        except pd.errors.EmptyDataError:
            print('Error: The file is \'{}\' empty.'.format(self.train_data_file))
        except pd.errors.ParserError:
            print('Error: There was a problem parsing the CSV file.')
        except Exception as e:
            print('An unexpected error occurred: \'{}\''.format(e))

    def __get_mean_std_data(self) -> pd.DataFrame | None:
        """
        Calculates and returns the mean and standard deviation for each column in the DataFrame.

        :return: A pandas DataFrame containing the mean and standard deviation for each column.
        """
        return self.df.agg(['mean', 'std']).transpose()

    @property
    def train_data_file(self) -> str:
        """
        Gets the path to the training data file.

        :return: The path to the training data file.
        """
        return self._train_data_file

    @train_data_file.setter
    def train_data_file(self, new_value: str):
        """
        Sets the path to the training data file.

        :param new_value: The new path to the training data file.
        :raises ValueError: If the new value is empty.
        :raises TypeError: If the new value is not a string.
        """
        if not new_value:
            raise ValueError('Name of the file cannot be empty.')

        if not isinstance(new_value, str):
            raise TypeError('File name must be a string. Instead got {}.'.format(type(new_value)))

        self._train_data_file = new_value

    @property
    def threshold(self) -> int:
        """
        Gets the threshold for anomaly detection.

        :return: The threshold for anomaly detection.
        """
        return self._threshold

    @threshold.setter
    def threshold(self, new_value: int):
        """
        Sets the threshold for anomaly detection.

        :param new_value: The new threshold value.
        :raises TypeError: If the new value is not an integer.
        """
        if not isinstance(new_value, int):
            raise TypeError('Threshold must be an integer. Instead got {}.'.format(type(new_value)))

        self._threshold = new_value