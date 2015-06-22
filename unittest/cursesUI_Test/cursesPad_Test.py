import nose
import BaseTestCase
from mock import Mock, patch
from cursesUI import cursesPad


class cursesPad_Test(BaseTestCase.BaseTestCase):

    @patch('cursesUI.cursesPad.os.popen')
    def setUp(self, mock_popen):
        super(self.__class__, self).setUp()
        reader = Mock()
        reader.read.side_effect = ["1200 1300"]
        mock_popen.return_value = reader

        self.test_pad = cursesPad.cursesPad()

    def test_should_instantiate(self):
        assert(isinstance(self.test_pad, cursesPad.cursesPad))

    def test_pad_should_be_part_of_the_borg_collective(self):
        pad1 = cursesPad.cursesPad()
        pad2 = cursesPad.cursesPad()

        pad1.test = "test"

        assert(pad2.test == "test")

    @patch('cursesUI.cursesPad.curses.newpad')
    def test_initialize_should_call_curses_newpad_correctly(self, mock_curses):

        self.test_pad.initialize()

        mock_curses.assert_called_with(10000, 1300 - 2)

    def test_addStr_should_update_internal_pad_without_color_args_correctly(self):
        self.test_pad.pad = Mock()

        self.test_pad.addStr("test")

        self.test_pad.pad.addstr.assert_called_with("test")

    @patch('cursesUI.cursesPad.curses')
    def test_addStr_should_internal_pad_with_color_args_correctly(self, mock_curses):
        self.test_pad.pad = Mock()
        mock_curses.color_pair.return_value = 2

        self.test_pad.addStr("test", 2)

        self.test_pad.pad.addstr.assert_called_with("test", 2)

    @patch('cursesUI.cursesPad.curses')
    def test_calls_to_addStr_with_color_should_ignore_exceptions(self, mock_curses):
        self.test_pad.pad = Mock()
        self.test_pad.pad.addstr.side_effect = Exception("Test Exception")
        mock_curses.color_pair.return_value = 2

        self.test_pad.addStr("test", 2)

        self.test_pad.pad.addstr.assert_called_with("test", 2)

    def test_calls_to_addStr_without_color_should_ignore_exceptions(self):
        self.test_pad.pad = Mock()
        self.test_pad.pad.addstr.side_effect = Exception("Test Exception")

        self.test_pad.addStr("test")

        self.test_pad.pad.addstr.assert_called_with("test")

    def test_addString_should_update_internal_pad_without_color_args_correctly(self):
        self.test_pad.pad = Mock()

        self.test_pad.addString(0, 0, "test")

        self.test_pad.pad.addstr.assert_called_with(0, 0, "test")

    @patch('cursesUI.cursesPad.curses')
    def test_addString_should_update_internal_pad_with_color_args_correctly(self, mock_curses):
        self.test_pad.pad = Mock()
        mock_curses.color_pair.return_value = 2

        self.test_pad.addString(0, 0, "test", 2)

        self.test_pad.pad.addstr.assert_called_with(0, 0, "test", 2)

    @patch('cursesUI.cursesPad.curses')
    def test_calls_to_addString_with_color_should_ignore_exceptions(self, mock_curses):
        self.test_pad.pad = Mock()
        mock_curses.color_pair.return_value = 2
        self.test_pad.pad.addstr.side_effect = Exception("Test Exception")

        self.test_pad.addString(0, 0, "test", 2)

        self.test_pad.pad.addstr.assert_called_with(0, 0, "test", 2)

    def test_calls_to_addString_without_color_should_ignore_exceptions(self):
        self.test_pad.pad = Mock()
        self.test_pad.pad.addstr.side_effect = Exception("Test Exception")

        self.test_pad.addString(0, 0, "test")

        self.test_pad.pad.addstr.assert_called_with(0, 0, "test")

    def test_refresh_should_refresh_pad_content_to_window(self):
        self.test_pad.pad = Mock()

        self.test_pad.refresh(1)

        self.test_pad.pad.noutrefresh.assert_called_with(1, 0, 4, 0, int(self.test_pad.size[0]) - 2, int(self.test_pad.size[1]) - 2)

    def test_refresh_should_ignore_exceptions(self):
        self.test_pad.pad = Mock()
        self.test_pad.pad.noutrefresh.side_effect = Exception("Test Exception")

        self.test_pad.refresh(1)

        self.test_pad.pad.noutrefresh.assert_called_with(1, 0, 4, 0, int(self.test_pad.size[0]) - 2, int(self.test_pad.size[1]) - 2)

    def test_draw_should_not_process_empty_instructions(self):
        self.test_pad.addString = Mock()
        self.test_pad.addStr = Mock()

        self.test_pad.draw([])

        assert not self.test_pad.addString.called
        assert not self.test_pad.addStr.called

    def test_draw_should_handle_2_tuple_long_instructions(self):
        self.test_pad.addString = Mock()
        self.test_pad.addStr = Mock()

        self.test_pad.draw([("test_string", 2)])

        self.test_pad.addStr.assert_called_with("test_string", 2)
        assert not self.test_pad.addString.called

    def test_draw_should_handle_4_tuple_long_instructions(self):
        self.test_pad.addString = Mock()
        self.test_pad.addStr = Mock()

        self.test_pad.draw([(1, 2, "test_string", 3)])

        self.test_pad.addString.assert_called_with(1, 2, "test_string", 3)
        assert not self.test_pad.addStr.called

    def test_clear_should_clear_curses_pad(self):
        self.test_pad.pad = Mock()

        self.test_pad.clear()

        self.test_pad.pad.clear.assert_called_with()

if __name__ == '__main__':
    nose.runmodule()