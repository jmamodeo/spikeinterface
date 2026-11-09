import sys
import unittest
from unittest.mock import MagicMock, patch

import pytest

from spikeinterface.sorters import Mountainsort5Sorter


class TestMountainsort5RandomSeed(unittest.TestCase):
    def test_random_seed_in_default_params(self):
        params = Mountainsort5Sorter.default_params()
        assert "random_seed" in params
        assert params["random_seed"] is None
        assert "random_seed" in Mountainsort5Sorter.params_description()

    def test_random_seed_requires_ms5_0_5_10(self):
        params = Mountainsort5Sorter.default_params()
        params["random_seed"] = 17
        # mountainsort5 must import successfully before the version gate runs.
        sys.modules.setdefault("mountainsort5", MagicMock())
        with (
            patch(
                "spikeinterface.sorters.external.mountainsort5.version",
                return_value="0.5.9",
            ),
            pytest.raises(ValueError, match="random_seed.*0\\.5\\.10"),
        ):
            Mountainsort5Sorter._run_from_folder(
                sorter_output_folder=None,
                params=params,
                verbose=False,
            )


if __name__ == "__main__":
    unittest.main()
