import xlrd
from django.utils.six.moves import range

class XlsImportHelper():

    def __init__(self, **kwargs):
        if 'file_path' in kwargs:
            with xlrd.open_workbook(kwargs.get('file_path')) as excel_file:
                self._workbook = excel_file
                self.setSheet(**kwargs)
        elif 'workbook' in kwargs:
            self._workbook = kwargs.get('workbook')
            self.setSheet(**kwargs)
        elif 'sheet' in kwargs:
            this._sheet = kwargs.get('sheet')
        else:
            raise ValueError("Worksheet can't be found") #raise and error if file_path not provided

    def getRowColumnNo(self, *args, **kwargs):
        """
            Return a tupple for the rownum and columnnum of the searched string
        """
        search_string = kwargs.get('string')
        for rownum in range(self._sheet.nrows): #check on every row
            column_counter = 0
            for cell_value in self._sheet.row_values(rownum): #check on every cell value
                if  search_string.lower() in cell_value.__str__().strip().lower():
                    return (rownum, column_counter)
                column_counter +=1
        return "" #if not found, return blank

    def getValueOfRowColNo(self, *args, **kwargs):
        """
            Given a rownum and columnum, which coming from getRowColumnNo method, return the value
        """
        rownum_p = kwargs.get('rownum')
        colnum_p = kwargs.get('colnum')
        for rownum in range(self._sheet.nrows): #check on every row
            if rownum == rownum_p:
                column_counter = 0
                for cell_value in self._sheet.row_values(rownum): #check on every cell value
                    if  column_counter == colnum_p:
                        return cell_value.__str__().strip()
                    column_counter +=1
        return "" #if not found, return blank

    def getSchoolIDRegionValue(self): #
        """
            get the school ID and region. Region is next to school ID column
        """
        school_id = ""
        region = ""
        school_id_found_flag = False #a flag that identifies if "School ID" cell has been found already
        for rownum in range(self._sheet.nrows): #check on every row
            for cell_value in self._sheet.row_values(rownum): #check on every cell value
                if cell_value.__str__().strip().lower() == "school id":
                    school_id_found_flag = True
                    continue #move to next column
                if school_id_found_flag and cell_value.__str__().strip() != "" and school_id == "":
                    school_id = self.removePeriodFromString(string=cell_value.__str__().strip())
                    continue #move to get Region Value
                if school_id_found_flag and cell_value.__str__().strip() != "":
                    region = cell_value.__str__().strip()
                    return {'school_id':school_id,'region':region}
        return {} #return empty dictionary

    def getValueHorizontalAdjacent(self, search_string):
        """
            Search for a string to be find, and get the next valid value adjacent to it
        """
        search_string_found_flag = False #a flag that identifies if search string has been found already
        for rownum in range(self._sheet.nrows): #check on every row
            for cell_value in self._sheet.row_values(rownum): #check on every cell value
                if cell_value.__str__().strip().lower() == search_string.lower():
                    search_string_found_flag = True
                    continue #move to next column
                if search_string_found_flag and cell_value.__str__().strip() != "":
                    return cell_value.__str__().strip()
        return "" #if not found, return blank

    def getValueVerticalAdjacent(self, search_string):
        """
            Search for a string to be find and get the next valid value of its vertical adjacent, vertical up
        """
        row_col_no = self.getRowColumnNo(string=search_string)
        if row_col_no != "":
            rownum = row_col_no[0] - 1
            return_value = self.getValueOfRowColNo(rownum=rownum, colnum=row_col_no[1])
            while return_value == '' and rownum >= 0: #iterate until valid value found, valid means not blank
                rownum -= 1
                return_value = self.getValueOfRowColNo(rownum=rownum, colnum=row_col_no[1])
            return return_value
        else:
            return ""

    def removePeriodFromString(self, *args, **kwargs):
        return kwargs.get('string').split(".")[0]

    def setSheet(self, *args, **kwargs):
        if 'sheet_index' in kwargs:
            self._sheet = self._workbook.sheet_by_index(kwargs.get('sheet_index')) #get the index number provided
                                                                                    #need to improve, raise error of specified index is greater than available indexes
        else:
            self._sheet = self._workbook.sheet_by_index(0) #if not provided, default to first sheet
