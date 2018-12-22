import tempfile

from xlsxreporter import BaseReport, ReportContext, row_renderer


def test_render_empty():
    class EmptyReport(BaseReport):
        title = "Empty report"

        def generate_rows(self):
            yield self.render_empty()

    with tempfile.TemporaryFile() as f:
        context = ReportContext("filename.xlsx", outfile=f)
        with context:
            context.add_report(EmptyReport())

        assert len(context.workbook.worksheets()) == 1
        assert context.workbook.get_worksheet_by_name(EmptyReport.title)

        f.seek(0)
        assert f.read()


def test_render_simple():
    class SimpleReport(BaseReport):
        title = "Simple report"

        def generate_rows(self):
            yield self.render_rows()

        @row_renderer
        def render_rows(self, *, ctx, add_format):
            fmt = add_format({"align": "center"})
            ctx.write(ctx.row, 0, "Hello", fmt)
            ctx.write(ctx.row + 1, 0, "reporting", fmt)
            return 2

    with tempfile.TemporaryFile() as f:
        context = ReportContext("filename.xlsx", outfile=f)
        with context:
            context.add_report(SimpleReport())

        assert len(context.workbook.worksheets()) == 1
        assert context.workbook.get_worksheet_by_name(SimpleReport.title)

        f.seek(0)
        assert f.read()
