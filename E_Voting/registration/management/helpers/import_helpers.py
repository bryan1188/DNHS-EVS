import xlrd
from django.utils.six.moves import range

class XlsImportHelper():
    """
        Helper class that will read the existing xls file used by the school. It provides several methods to help find each value in the file.
    """

    def __init__(self, **kwargs):
        """
            paramters: file_path, workbook, sheet
        """

        if 'file_path' in kwargs:
            with xlrd.open_workbook(kwargs.get('file_path')) as excel_file:
                self._workbook = excel_file
                self.setSheet(**kwargs)
        elif 'workbook' in kwargs:
            self._workbook = kwargs.get('workbook')
            self.setSheet(**kwargs)
        elif 'sheet' in kwargs:
            self._sheet = kwargs.get('sheet')
        else:
            raise ValueError("Worksheet can't be found") #raise and error if file_path not provided

    def getBoSY(self):
        """
            get BoSY numbers. MALE, FEMALE, and TOTAL. return dictionary
        """
        row_col_no = self.getRowColumnNo(search_string="BoSY",wild_search=False)
        return {
                'male': self.removePeriodFromString(string=self.getValueOfRowColNo(rownum=row_col_no[0]+1, colnum=row_col_no[1])),
                'female': self.removePeriodFromString(string=self.getValueOfRowColNo(rownum=row_col_no[0]+4, colnum=row_col_no[1])),
                'total': self.removePeriodFromString(string=self.getValueOfRowColNo(rownum=row_col_no[0]+6, colnum=row_col_no[1])),
                }

    def getEoSY(self):
        """
            get EoSY numbers. MALE, FEMALE, and TOTAL. return dictionary
        """
        row_col_no = self.getRowColumnNo(search_string="EoSY",wild_search=False)
        return {
                'male': self.removePeriodFromString(string=self.getValueOfRowColNo(rownum=row_col_no[0]+1, colnum=row_col_no[1])),
                'female': self.removePeriodFromString(string=self.getValueOfRowColNo(rownum=row_col_no[0]+4, colnum=row_col_no[1])),
                'total': self.removePeriodFromString(string=self.getValueOfRowColNo(rownum=row_col_no[0]+6, colnum=row_col_no[1])),
                }

    def getRowColumnNo(self, *args, **kwargs):
        """
            Return a tupple for the rownum and columnnum of the searched string
            parameters: search_string, wild_search(default True)
        """
        search_string = kwargs.get('search_string')
        wild_search = kwargs.get('wild_search', True)
        for rownum in range(self._sheet.nrows): #check on every row
            column_counter = 0
            for cell_value in self._sheet.row_values(rownum): #check on every cell value
                if wild_search:
                    if  search_string.lower() in cell_value.__str__().strip().lower():
                        return (rownum, column_counter)
                else:
                    if  search_string.lower() == cell_value.__str__().strip().lower():
                        return (rownum, column_counter)
                column_counter +=1
        return "" #if not found, return blank

    def getValueOfRowColNo(self, *args, **kwargs):
        """
            Given a rownum and columnum, which coming from getRowColumnNo method, return the value
            parameters: rownum, colnum
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
            return a dicationary {'school_id':vale, 'region':region}
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

    def getValueHorizontalAdjacent(self, **kwargs):
        """
            Search for a string to be find, and get the next valid value horizontally adjacent to it
        """
        search_string = kwargs.get('search_string')
        search_string_found_flag = False #a flag that identifies if search string has been found already
        for rownum in range(self._sheet.nrows): #check on every row
            for cell_value in self._sheet.row_values(rownum): #check on every cell value
                if cell_value.__str__().strip().lower() == search_string.lower():
                    search_string_found_flag = True
                    continue #move to next column
                if search_string_found_flag and cell_value.__str__().strip() != "":
                    return cell_value.__str__().strip()
        return "" #if not found, return blank

    def getValueVerticalAdjacent(self, **kwargs):#search_string, up_direction=True):
        """
            Search for a string to be found and get the next valid value of its vertical adjacent, vertical up or vertical down
            paramters: search_string,up_direction(default=True),wild_search(default=False)
        """
        search_string = kwargs.get('search_string')
        up_direction = kwargs.get('up_direction', True)
        if up_direction:
            delta = -1
        else:
            delta = 1

        row_col_no = self.getRowColumnNo(**kwargs)
        if row_col_no != "":
            rownum = row_col_no[0] + delta
            return_value = self.getValueOfRowColNo(rownum=rownum, colnum=row_col_no[1])
            while return_value == '' and rownum >= 0 and rownum <= self._sheet.nrows: #iterate until valid value found, valid means not blank
                rownum += delta
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
