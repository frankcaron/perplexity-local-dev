from main import main


def test_main_runs():
    import io
    from contextlib import redirect_stdout

    buffer = io.StringIO()
    with redirect_stdout(buffer):
        main()

    assert buffer.getvalue() == "Hello, world!\n"
