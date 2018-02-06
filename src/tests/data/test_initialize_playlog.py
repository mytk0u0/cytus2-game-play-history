# coding: utf-8

import mock
import pytest
from src.data.initialize_playlog import main


class MainTest(object):
    @mock.patch('os.path.exists', return_value=True)
    def test_do_nothing_when_file_exists(
            self,
            m_exists: mock.MagicMock,
            ) -> None:
        with pytest.raises(FileExistsError):
            main()

    @mock.patch('builtins.open', new_callable=mock.mock_open())
    @mock.patch('os.path.exists', return_value=False)
    def test_make_new_csv_when_file_not_exists(
            self,
            m_exists: mock.MagicMock,
            m_open: mock.MagicMock
            ) -> None:
        main()
