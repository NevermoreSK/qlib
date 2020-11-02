# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import mlflow
from pathlib import Path
from .recorder import MLflowRecorder


class Experiment:
    """
    Thie is the `Experiment` class for each experiment being run. The API is designed
    """

    def __init__(self):
        self.name = None
        self.id = None
        self.recorders = list()

    def create_recorder(self):
        """
        Create a recorder for each experiment.

        Parameters
        ----------

        Returns
        -------
        A recorder instance.
        """
        raise NotImplementedError(f"Please implement the `create_recorder` method.")

    def search_records(self, **kwargs):
        """
        Get a pandas DataFrame of records that fit the search criteria of the experiment.

        Parameters
        ----------
        filter_string : str
            filter query string, defaults to searching all runs.
        run_view_type : int
            one of enum values ACTIVE_ONLY, DELETED_ONLY, or ALL (e.g. in mlflow.entities.ViewType).
        max_results  : int
            the maximum number of runs to put in the dataframe.
        order_by : list
            list of columns to order by (e.g., “metrics.rmse”).

        Returns
        -------
        A pandas.DataFrame of records.
        """
        raise NotImplementedError(f"Please implement the `search_records` method.")

    def delete_recorder(self, rid):
        """
        Create a recorder for each experiment.

        Parameters
        ----------
        rid : str
            the id of the recorder to be deleted.

        Returns
        -------
        A recorder instance.
        """
        raise NotImplementedError(f"Please implement the `delete_recorder` method.")


class MLflowExperiment(Experiment):
    """
    Use mlflow to implement Experiment.
    """

    def create_recorder(self):
        recorder = MLflowRecorder(self.id)
        self.recorders.append(recorder)
        return recorders

    def search_records(self, **kwargs):
        filter_string = "" if kwargs.get("filter_string") is None else kwargs.get("filter_string")
        run_view_type = 1 if kwargs.get("run_view_type") is None else kwargs.get("run_view_type")
        max_results = 100000 if kwargs.get("max_results") is None else kwargs.get("max_results")
        order_by = kwargs.get("order_by")
        return mlflow.search_runs([self.experiment_id], filter_string, run_view_type, max_results, order_by)

    def delete_recorder(self, rid):
        mlflow.delete_run(rid)
        self.recorders = [r for r in self.recorders if r.recorder_id == rid]