import gspread
import itertools

from credentials import google_api_credentials

class gSpreadSheet:

	client_ = None

	def __init__(self, auth):

		if auth is not None:
			credentials_ = google_api_credentials(auth)
			self.client_ = gspread.authorize(credentials_)


	""" spreadsheet check exist. """
	def is_spreadsheet_exist(self, spreadsheet):

		try:
			_ss = self.client_.open(spreadsheet)
			return _ss
		except gspread.SpreadsheetNotFound:
			pass
		return None


	""" worksheet check exist. """
	def is_worksheet_exist(self, spreadsheet, worksheet):

		_ss = self.is_spreadsheet_exist(spreadsheet)
		if _ss:
			try:
				_ws = _ss.worksheet(worksheet)
				return _ws
			except gspread.WorksheetNotFound:
				pass
		return None


	""" worksheet to list in list table. """
	def sheet2table(self, spreadsheet, worksheet, start_rows=1, start_cols=1, want_rows=0, want_cols=0):

		# spreadsheet
		_ss = self.is_spreadsheet_exist(spreadsheet)
		if _ss is None:
			return None

		# worksheet
		_ws = self.is_worksheet_exist(spreadsheet, worksheet)
		if _ws is None:
			return None

		_rows = _ws.row_count
		_cols = _ws.col_count

		_cells = _ws.range(1, 1, _rows, _cols)
		return gspread.utils.cell_list_to_rect(_cells)


	""" list in list table to worksheet. """
	def table2sheet(self, table, spreadsheet, worksheet, create_sheet=True):

		_rows = len(table)
		if _rows > 0:
			_cols = len(table[0])
		else:
			return
		if _cols < 1:
			return

		_ss = self.is_spreadsheet_exist(spreadsheet)
		if _ss is None:
			if create_sheet:
				_ss = self.client_.create(spreadsheet)
				_ws = _ss.sheet1
				_ws.update_title(worksheet)
			else:
				raise gspread.SpreadsheetNotFound
		else:
			_ws = self.is_worksheet_exist(spreadsheet, worksheet)
			if _ws is None:
				if create_sheet:
					_ws = _ss.add_worksheet(title=worksheet, rows=_rows, cols=_cols)
				else:
					raise gspread.WorksheetNotFound

		_rowcol = gspread.utils.rowcol_to_a1(_rows, _cols)
		_ws.resize(rows=_rows, cols=_cols)
		_cells = _ws.range('A1:'+_rowcol)
		#print(_cells)
		_upd_vals = list(itertools.chain.from_iterable(table))
		for _idx, _cell in enumerate(_cells):
			_cell.value = _upd_vals[_idx]
		_ws.update_cells(_cells)


if __name__ == '__main__':
	_gs = gSpreadSheet("token_gspread.pickle")
	_table = _gs.sheet2table('test4gspread', 'worksheet1')
	_trans = []
	for _each in _table:
		_trans.append(gspread.utils.numericise_all(_each))
	#print(_trans)
	_gs.table2sheet(_trans, 'test4gspread', 'worksheet1')
