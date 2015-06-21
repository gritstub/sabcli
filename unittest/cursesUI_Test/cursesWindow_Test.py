import nose
import BaseTestCase
from mock import Mock, patch
from cursesUI import cursesWindow
from cursesUI.cursesPad import cursesPad


class cursesWindow_Test(BaseTestCase.BaseTestCase):

    @patch('cursesUI.cursesWindow.os.popen')
    def setUp(self, mock_popen):
        super(self.__class__, self).setUp()
        reader = Mock()
        reader.read.side_effect = ["1200 1300"]
        mock_popen.return_value = reader

        self.test_window = cursesWindow.cursesWindow(pad=Mock(spec=cursesPad))

    def test_should_instantiate(self):
        assert(isinstance(self.test_window, cursesWindow.cursesWindow))

    def test_initialize_should_setup_windows(self):
        self.test_window.initializeWindow = Mock()
        self.test_window.initializeColorScheme = Mock()

        self.test_window.initialize()

        self.test_window.initializeWindow.assert_called_with()

    def test_initialize_should_setup_color_scheme(self):
        self.test_window.initializeWindow = Mock()
        self.test_window.initializeColorScheme = Mock()

        self.test_window.initialize()

        self.test_window.initializeColorScheme.assert_called_with()

    @patch('cursesUI.cursesWindow.curses')
    def test_initialiseWindow_should_initialize_screen(self, mock_curses):

        self.test_window.initializeWindow()

        mock_curses.initscr.assert_called_with()

    @patch('cursesUI.cursesWindow.curses')
    def test_initialiseWindow_should_enable_color(self, mock_curses):

        self.test_window.initializeWindow()

        mock_curses.start_color.assert_called_with()
        mock_curses.use_default_colors.assert_called_with()

    @patch('cursesUI.cursesWindow.curses')
    def test_initialiseWindow_should_configure_curses_to_not_write_keyboard_input_to_the_screen(self, mock_curses):

        self.test_window.initializeWindow()

        mock_curses.noecho.assert_called_with()

    @patch('cursesUI.cursesWindow.curses')
    def test_initialiseWindow_should_configure_curses_to_react_on_keypress(self, mock_curses):

        self.test_window.initializeWindow()

        mock_curses.cbreak.assert_called_with()

    @patch('cursesUI.cursesWindow.curses')
    def test_initialiseWindow_should_configure_curses_to_interpret_advanced_keys(self, mock_curses):

        self.test_window.initializeWindow()

        self.test_window.screen.keypad.assert_was_called(1)

    @patch('cursesUI.cursesWindow.curses')
    def test_initialiseWindow_should_hide_cursor(self, mock_curses):
        self.test_window.setCursorVisibility = Mock()
        self.test_window.initializeWindow()

        self.test_window.setCursorVisibility.assert_was_called(0)

    @patch('cursesUI.cursesWindow.curses')
    def test_initialiseWindow_should_setup_window(self, mock_curses):

        self.test_window.initializeWindow()

        mock_curses.newwin.assert_called_with(int(self.test_window.size[0]), int(self.test_window.size[1]), 0, 0)

    @patch('cursesUI.cursesWindow.curses')
    @patch('cursesUI.cursesWindow.signal')
    def test_initialiseWindow_should_setup_window(self, mock_signal, mock_curses):

        self.test_window.initializeWindow()

        mock_signal.signal.assert_called_with(mock_signal.SIGWINCH, self.test_window.windowSizeChangeEventHandler)

    @patch('cursesUI.cursesWindow.curses')
    def test_initializeColorScheme_should_setup_custom_colors(self, mock_curses):

        self.test_window.initializeColorScheme()

        assert mock_curses.init_pair.called

    @patch('cursesUI.cursesWindow.os.popen')
    def test_windowSizeChangeHandler_should_update_window_size(self, mock_popen):
        reader = Mock()
        reader.read.side_effect = ["1000 1400"]
        mock_popen.return_value = reader

        self.test_window.windowSizeChangeEventHandler('', '')

        assert self.test_window.size == ["1000", "1400"]

    def test_getUserInput_should_get_keyboard_input_from_curses_screen(self):
        self.test_window.screen = Mock()

        self.test_window.getUserInput()

        self.test_window.screen.getch.assert_called_with()

    @patch('cursesUI.cursesWindow.curses')
    def test_close_should_make_cursor_visible_again(self, mock_curses):
        self.test_window.setCursorVisibility = Mock()
        self.test_window.screen = Mock()

        self.test_window.close()

        self.test_window.setCursorVisibility.assert_called_with(1)

    @patch('cursesUI.cursesWindow.curses')
    def test_close_should_reenable_return_press_for_action(self, mock_curses):
        self.test_window.setCursorVisibility = Mock()
        self.test_window.screen = Mock()

        self.test_window.close()

        mock_curses.nocbreak.assert_called_with()

    @patch('cursesUI.cursesWindow.curses')
    def test_close_should_disable_interpretation_of_special_keypresses(self, mock_curses):
        self.test_window.setCursorVisibility = Mock()
        self.test_window.screen = Mock()

        self.test_window.close()

        self.test_window.screen.keypad.assert_called_with(0)


    @patch('cursesUI.cursesWindow.curses')
    def test_close_should_reenable_showing_all_keyboard_presses_on_screen(self, mock_curses):
        self.test_window.setCursorVisibility = Mock()
        self.test_window.screen = Mock()

        self.test_window.close()

        mock_curses.echo.assert_called_with()

    @patch('cursesUI.cursesWindow.curses')
    def test_close_should_shutdown_window(self, mock_curses):
        self.test_window.setCursorVisibility = Mock()
        self.test_window.screen = Mock()

        self.test_window.close()

        mock_curses.endwin.assert_called_with()

    @patch('cursesUI.cursesWindow.curses')
    def test_getInput_should_enable_cursor(self, mock_curses):
        self.test_window.setCursorVisibility = Mock()

        self.test_window.getInput("")

        self.test_window.setCursorVisibility.assert_any_call(1)

    @patch('cursesUI.cursesWindow.curses')
    def test_getInput_should_get_user_input_from_curses_textpad(self, mock_curses):
        self.test_window.setCursorVisibility = Mock()

        self.test_window.getInput("")

        mock_curses.textpad.Textbox.assert_called_with('', insert_mode=True)

    @patch('cursesUI.cursesWindow.curses')
    def test_getInput_should_disable_cursor_on_exit(self, mock_curses):
        self.test_window.setCursorVisibility = Mock()

        self.test_window.getInput("")

        self.test_window.setCursorVisibility.assert_called_with(0)

    @patch('cursesUI.cursesWindow.curses')
    def test_wait_should_set_timeout_on_screen(self, mock_curses):
        self.test_window.screen = Mock()

        self.test_window.wait(1200)

        self.test_window.screen.timeout.assert_called_with(1200)

    @patch('cursesUI.cursesWindow.curses')
    def test_update_should_force_update_of_curses(self, mock_curses):
        self.test_window.screen = Mock()

        self.test_window.update()

        mock_curses.doupdate.assert_called_with()

    @patch('cursesUI.cursesWindow.curses')
    def test_refresh_should_draw_screen(self, mock_curses):
        self.test_window.screen = Mock()

        self.test_window.refresh(1)

        self.test_window.screen.noutrefresh.assert_called_with()

    @patch('cursesUI.cursesWindow.curses')
    def test_refresh_should_ignore_exceptions_from_screen(self, mock_curses):
        self.test_window.screen = Mock()
        self.test_window.screen.noutrefresh.side_effect = Exception("Test Exception")

        self.test_window.refresh(1)

        self.test_window.screen.noutrefresh.assert_called_with()

    @patch('cursesUI.cursesWindow.curses')
    def test_update_should_force_drawing_of_pad(self, mock_curses):
        self.test_window.screen = Mock()

        self.test_window.refresh(1)

        self.test_window.pad.refresh.assert_called_with(1)

    @patch('cursesUI.cursesWindow.curses')
    def test_update_should_force_update_of_curses(self, mock_curses):
        self.test_window.screen = Mock()

        self.test_window.update()

        mock_curses.doupdate.assert_called_with()

    def test_clear_should_clear_contents_of_screen(self):
        self.test_window.screen = Mock()

        self.test_window.clear()

        self.test_window.screen.clear.assert_called_with()

    def test_clear_should_clear_contents_of_pad(self):
        self.test_window.screen = Mock()

        self.test_window.clear()

        self.test_window.pad.clear.assert_called_with()

    def test_addStr_should_update_internal_screen_without_color_args_correctly(self):
        self.test_window.screen = Mock()

        self.test_window.addStr("test")

        self.test_window.screen.addstr.assert_called_with("test")

    @patch('cursesUI.cursesWindow.curses')
    def test_addStr_should_update_internal_screen_with_color_args_correctly(self, mock_curses):
        self.test_window.screen = Mock()
        mock_curses.color_pair.return_value = 2

        self.test_window.addStr("test", 2)

        self.test_window.screen.addstr.assert_called_with("test", 2)

    @patch('cursesUI.cursesWindow.curses')
    def test_calls_to_addStr_with_color_should_ignore_exceptions(self, mock_curses):
        self.test_window.screen = Mock()
        mock_curses.color_pair.return_value = 2
        self.test_window.screen.addstr.side_effect = Exception("Test Exception")

        self.test_window.addStr("test", 2)

        self.test_window.screen.addstr.assert_called_with("test", 2)

    def test_calls_to_addStr_without_color_should_ignore_exceptions(self):
        self.test_window.screen = Mock()
        self.test_window.screen.addstr.side_effect = Exception("Test Exception")

        self.test_window.addStr("test")

        self.test_window.screen.addstr.assert_called_with("test")

    def test_addString_should_update_internal_screen_without_color_args_correctly(self):
        self.test_window.screen = Mock()

        self.test_window.addString(0, 0, "test")

        self.test_window.screen.addstr.assert_called_with(0, 0, "test")

    @patch('cursesUI.cursesWindow.curses')
    def test_addString_should_update_internal_screen_with_color_args_correctly(self, mock_curses):
        self.test_window.screen = Mock()
        mock_curses.color_pair.return_value = 2

        self.test_window.addString(0, 0, "test", 2)

        self.test_window.screen.addstr.assert_called_with(0, 0, "test", 2)

    @patch('cursesUI.cursesWindow.curses')
    def test_calls_to_addString_with_color_should_ignore_exceptions(self, mock_curses):
        self.test_window.screen = Mock()
        mock_curses.color_pair.return_value = 2
        self.test_window.screen.addstr.side_effect = Exception("Test Exception")

        self.test_window.addString(0, 0, "test", 2)

        self.test_window.screen.addstr.assert_called_with(0, 0, "test", 2)

    def test_calls_to_addString_without_color_should_ignore_exceptions(self):
        self.test_window.screen = Mock()
        self.test_window.screen.addstr.side_effect = Exception("Test Exception")

        self.test_window.addString(0, 0, "test")

        self.test_window.screen.addstr.assert_called_with(0, 0, "test")

    def test_draw_should_not_process_empty_instructions(self):
        self.test_window.addString = Mock()
        self.test_window.addStr = Mock()

        self.test_window.draw([])

        assert not self.test_window.addString.called
        assert not self.test_window.addStr.called

    def test_draw_should_handle_2_tuple_long_instructions(self):
        self.test_window.addString = Mock()
        self.test_window.addStr = Mock()

        self.test_window.draw([("test_string", 2)])

        self.test_window.addStr.assert_called_with("test_string", 2)
        assert not self.test_window.addString.called

    def test_draw_should_handle_4_tuple_long_instructions(self):
        self.test_window.addString = Mock()
        self.test_window.addStr = Mock()

        self.test_window.draw([(1, 2, "test_string", 3)])

        self.test_window.addString.assert_called_with(1, 2, "test_string", 3)
        assert not self.test_window.addStr.called

if __name__ == '__main__':
    nose.runmodule()