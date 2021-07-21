# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 14:26:21 2016

@author: fst

start a connection to a ODBC Database
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

#import pyodbc

import sys
import datetime
#import time
from datetime import timedelta
import logging
import pandas as pd
import configparser
import warnings
#import traceback
from collections import OrderedDict
#import itertools
#from operator import itemgetter
import numpy as np
from datetime import datetime as dt

from sqlalchemy import create_engine

logger = logging.getLogger(__name__)


class EbcSql(object):
    def __init__(self, server=None, port=None, database=None, user=None, password=None,
                 driver=None, dialect=None, engine=None,
                 option_files=None, option_groups=None):
        """
        Class:          EbcOdbc
        Description:    connection to ODBC database
        ########
        Inputs
        ########
        Variable:       Server
        Description:    Server of ODBC database
        Type:           str
        ########
        Variable:       Port
        Description:    Port of ODBC database
        Type:           str
        ########
        Variable:       Database
        Description:    Database name of ODBC database
        Type:           str
        ########
        Variable:       User
        Description:    User of ODBC database
        Type:           str
        ########
        Variable:       Password
        Description:    Password of user of ODBC database
        Type:           str
        ########
        Variable:       Driver
        Description:    Driver of ODBC database
        Type:           str
        Standard:       ODBC Driver for SQL Server
        """
        self.connection = None
        self.extra_parameter = {}
        """initialize settings for timeseries"""
        self.ts_database = None
        self.ts_table = None
        self.ts_time_column = None
        self.ts_value_column = None
        self.ts_itemid_column = None
        self.ts_chosen_key = None
        self.ts_quality_id_column = None
        self.ts_quality_id = None
        
        self.item_database = None
        self.item_table = None
        self.item_itemid_column = None
        self.item_itemname_column = None
        self.time_format = None
        
        
        
        
        """initialize settings for items table (timeseries)"""
        self.item_database = None
        self.item_table = None
        self.item_itemid_column = None
        self.item_itemname_column = None
        self.time_format = None
        self.server = None
        self.port = None
        self.database = None
        self.user = None
        self.password = None
        self.driver = None
        self.dialect = None
        self.engine = None

        if option_files is not None:
            self._set_connection(option_files, option_groups)
            self.connect()
        else:
            self.server = server
            self.port = port
            self.database = database
            self.user = user
            self.password = password
            self.driver = driver
            self.dialect = dialect
            self.engine = engine
            """"connect to database"""
            self.connect()
        
    def _set_connection(self, option_files=None, option_groups=None):
        """
        function:       _set_connection
        Description:    set variables for odbc connection configuration with config file in path
        ########
        Inputs
        ########
        Variable:       option_files
        Description:    The path to the extra configuration file
        Type:           str
        ########
        Variable:       option_groups
        Description:    The groups of the extra configuration , which will be read
        Type:           str
        ########
        No Outputs
        ########
        """
        if option_files is not None:
            if type(option_files) is str:
                option_files = [option_files]
            if type(option_groups) is str:
                option_groups = [option_groups]
            for each_file in option_files:
                config = configparser.ConfigParser()
                config.optionxform = str
                config.read(each_file)
                for each_section in config.sections():
                    if (option_groups is None or (option_groups is not None and
                                                  each_section in option_groups)):
                        for (each_key, each_val) in config.items(each_section):
                            """set default variables"""
                            if each_key in ["SERVER", "server", "HOST", "host"]:
                                self.server = each_val
                            elif each_key in ["PORT", "port"]:
                                self.port = int(each_val)
                            elif each_key in ["DATABASE", "database", "DB", "db"]:
                                self.database = each_val
                            elif each_key in ["USER", "user", "UID", "uid"]:
                                self.user = each_val
                            elif each_key in ["PASSWORD", "password", "pwd", "PWD"]:
                                self.password = each_val
                            elif each_key in ["DRIVER", "driver"]:
                                self.driver = each_val
                            elif each_key in ["DIALECT", "dialect"]:
                                self.dialect = each_val
                            else:
                                self.extra_parameter[each_key] = each_val

    def set_engine(self):
        #dialect+driver://username:password@host:port/database    
        if self.driver!=None:
            engine_string="{}+{}".format(self.dialect, self.driver)
        else:
            engine_string=self.dialect
        engine_string="{}://{}:{}@{}:{}/{}".format(engine_string, self.user,
                                                   self.password, 
                                                   self.server, 
                                                   self.port, 
                                                   self.database)
        #print(engine_string)
        if len(self.extra_parameter)>0:
            self.engine = create_engine(engine_string, connect_args = self.extra_parameter)
        else:
            self.engine = create_engine(engine_string)
        return self.engine
    

    def set_standard(self, option_files, option_groups):
        """
        function:       set_standard
        Description:    set standard configuration variables for manual functions
                        of database with config file in path
        ########
        Inputs
        ########
        Variable:       option_files
        Description:    The path to the extra configuration file
        Type:           str
        ########
        Variable:       option_groups
        Description:    The groups of the extra configuration , which will be read
        Type:           str
        ########
        No Outputs
        ########
        Example for extra configuration in file:
            [timeseries]
            item_database=xxx
            item_table=item
            item_itemid_column=itemID
            item_itemname_column=itemname
            ts_database=xxx
            ts_table=measurement
            ts_time_column= timestamp
            ts_value_column= value
            ts_itemid_column= itemID
            #ts_quality_id_column=None
            ts_quality_id_column=qualityID
            ts_quality_id=192
            [format]
            time_format= %%Y-%%m-%%d %%H:%%M:%%S
        (for configuration it is important, that % will be set in %%)
        """
        """in this case option_groups:str or list"""
        if option_files is None:
            warnings.warn("No option files for extra parameter set", RuntimeWarning)
        if option_files is None:
            warnings.warn("No option groups for extra parameter set", RuntimeWarning)
        if type(option_files) is str:
            option_files = [option_files]
        if type(option_groups) is str:
            option_groups = [option_groups]
        for each_file in option_files:
            config = configparser.ConfigParser()
            config.read(each_file)
            for each_section in config.sections():
                if (option_groups is None or (option_groups is not None and
                                              each_section in option_groups)):
                    """settings for timeseries"""
                    if config.has_option(each_section, 'ts_database'):
                        self.ts_database = config[each_section]['ts_database']
                    if config.has_option(each_section, 'ts_table'):
                        self.ts_table = config[each_section]['ts_table']
                    if config.has_option(each_section, 'ts_time_column'):
                        self.ts_time_column = config[each_section]['ts_time_column']
                    if config.has_option(each_section, 'ts_value_column'):
                        self.ts_value_column = config[each_section]['ts_value_column']
                    if config.has_option(each_section, 'ts_itemid_column'):
                        self.ts_itemid_column = config[each_section]['ts_itemid_column']
                    if config.has_option(each_section, 'ts_chosen_key'):
                        self.ts_chosen_key = config[each_section]['ts_chosen_key']
                    if config.has_option(each_section, 'ts_quality_id_column'):
                        self.ts_quality_id_column = config[each_section]['ts_quality_id_column']
                    if config.has_option(each_section, 'ts_quality_id'):
                        self.ts_quality_id = config[each_section]['ts_quality_id']
                    if config.has_option(each_section, 'ts_columns'):
                        self.ts_columns = config[each_section]['ts_columns']
                    """settings for items table (timeseries)"""
                    if config.has_option(each_section, 'item_database'):
                        self.item_database = config[each_section]['item_database']
                    if config.has_option(each_section, 'item_table'):
                        self.item_table = config[each_section]['item_table']
                    if config.has_option(each_section, 'item_itemid_column'):
                        self.item_itemid_column = config[each_section]['item_itemid_column']
                    if config.has_option(each_section, 'item_itemname_column'):
                        self.item_itemname_column = config[each_section]['item_itemname_column']
                    if config.has_option(each_section, 'time_format'):
                        self.time_format = config[each_section]['time_format']
        return True

    def _get_ts_standard(self,
                         time_start=None,
                         time_end=None,
                         ts_database=None,
                         ts_table=None,
                         ts_time_column=None,
                         ts_value_column=None,
                         ts_itemid_column=None,
                         ts_chosen_key=None,
                         ts_quality_id_column=None,
                         ts_quality_id=None,
                         time_format=None):
        """get standard parameters for timeseries table"""
        try:
            if ts_database == None:
                ts_database = self.ts_database
            if ts_table == None:
                ts_table = self.ts_table
            if ts_time_column == None:
                ts_time_column = self.ts_time_column
            if ts_value_column == None:
                ts_value_column = self.ts_value_column
            if ts_itemid_column == None:
                ts_itemid_column = self.ts_itemid_column
            if ts_chosen_key == None:
                try:
                    ts_chosen_key = self.ts_chosen_key
                except:
                    pass
            if ts_quality_id_column == None:
                try:
                    ts_quality_id_column = self.ts_quality_id_column
                except:
                    pass
            if ts_quality_id == None:
                try:
                    ts_quality_id = self.ts_quality_id
                except:
                    pass
            if time_format == None:
                try:
                    time_format = self.time_format
                except:
                    warnings.warn("time format not in option_files, set to %%Y-%%m-%%d %%H:%%M:%%S", RuntimeWarning)
                    time_format = "%Y-%m-%d %H:%M:%S"
            if time_start == None:
                time_start = (dt.now() - timedelta(hours=1)).strftime(time_format)
            if time_end == None:
                time_end = dt.now().strftime(time_format)

        except KeyError:
            raise KeyError("not the right key parameters for function. Original Error: " + str(sys.exc_info()[2]))
        except:
            raise NameError("in the settings-file or in the function, some keys weren't defined. Original Error:" +
                            str(sys.exc_info()[2]))
        return (time_start, time_end, ts_database, ts_table, ts_time_column, ts_value_column, ts_itemid_column,
                ts_chosen_key, ts_quality_id_column, ts_quality_id, time_format)

    """get standard parameters for item table"""

    def _get_item_standard(self, item_database=None, item_table=None, item_itemid_column=None,
                           item_itemname_column=None):
        try:
            if item_database == None:
                item_database = self.item_database
            if item_table == None:
                item_table = self.item_table
            if item_itemid_column == None:
                item_itemid_column = self.item_itemid_column
            if item_itemname_column == None:
                item_itemname_column = self.item_itemname_column
        except:
            raise NameError("in the settings-file or in the function, some keys weren't defined. Original Error:" +
                            str(sys.exc_info()[2]))
        return item_database, item_table, item_itemid_column, item_itemname_column

    def connect(self):
        """connect to the database"""
        if self.engine is None:
            self.set_engine()
            self.connection = self.engine.connect()
        else:
            self.connection = self.engine.connect()

    def disconnect(self):
        """disconnect the connection"""
        self.connection.close()

    def close(self):
        """close the cursor"""
        try:
            self.connection.close()
            #self.cursor.close()
        except:
            pass

    def execute(self, execution_string):
        """
        Function:       execute
        Description:    execute execution_string in database
        #######
        Inputs:
        #######
        Variable:       execution_string
        Description:    command which will be executed
        Type:           str
        """
        data=self.connection.execute(execution_string)
        return data

    def commit(self):
        """
        Description:    commit changes to database
        """
        self.connection.commit()
    def execute_fetchall(self, execution_string, index_col=None):
        """
        function:       execute_fetchall
        Description:    execute execution_string and fetchall
        ########
        Inputs
        ########
        Variable:       execution_string
        Description:    String, which will be executed in database
        Type:           str
        ########
        Variable:       index_col
        Description:    column, which will be transformed to index
        Type:           str
        ########
        
        Outputs
        ########
        Variable:       data
        Description:    fetched data of mysql query
        Type:           list

        """
        #print(execution_string)
        data = pd.read_sql(execution_string,
                               con=self.connection,
                               index_col=index_col)
        return data
        

    def get_max(self, key=None, database=None, table=None):
        """
        function:       get_max
        Description:    get maximum of key in database.table
        ########
        Inputs
        ########
        Variable:       key
        Description:    name of chosen key
        Type:           str
        ########
        Variable:       database
        Description:    The database name to use
        Type:           str
        ########
        Variable:       table
        Description:    The table name to use
        Type:           str
        ########
        Outputs
        ########
        Variable:       data
        Description:    fetched maximum of chosen_key in odbc query
        Type:           depend on column
        """
        warnings.warn("get_max is deprecated, please use SQL in original", DeprecationWarning)
        if key==None:
            key=self.ts_chosen_key
        if database==None:
            database=self.database
        if table==None:
            table=self.ts_table
        
        execution_string = "SELECT MAX({}) AS {} FROM {}.{};".format(
            key, key, database, table)
        max_data = pd.read_sql(execution_string, con=self.connection).iloc[0,0]
        return max_data
        
    def get_min(self, key=None, database=None, table=None):
        """
        function:       get_max
        Description:    get maximum of key in database.table
        ########
        Inputs
        ########
        Variable:       key
        Description:    name of chosen key
        Type:           str
        ########
        Variable:       database
        Description:    The database name to use
        Type:           str
        ########
        Variable:       table
        Description:    The table name to use
        Type:           str
        ########
        Outputs
        ########
        Variable:       data
        Description:    fetched maximum of chosen_key in odbc query
        Type:           depend on column
        """
        warnings.warn("get_min is deprecated, please use SQL in original", DeprecationWarning)
        
        if key==None:
            key=self.ts_chosen_key
        if database==None:
            database=self.database
        if table==None:
            table=self.ts_table
        
        execution_string = "SELECT MIN({}) AS {} FROM {}.{};".format(
            key, key, database, table)
        max_data = pd.read_sql(execution_string, con=self.connection).iloc[0,0]
        return max_data   
        
        
    def get_max_number_data(self, start, format_string,
                            database=None, table=None, 
                            key=None):
        """
        get the maximal number of rows in database
        :param table_name: str : name of table
        :param key: str : name of chosen key column
        :param date_start:
        :param date_end:
        :param format_string:
        :return:
        """
        if database==None:
            database=self.ts_database
        if table==None:
            table=self.ts_table
        if key==None:
            key=self.ts_chosen_key
        
        if isinstance(start, str):
            start = datetime.datetime.strptime(start, format_string)
        
        if isinstance(start, datetime.datetime):
            execution_string = "select count(*) from {}.{} where {} >= '{}';".format(
                database, table, 
                key, start.strftime(format_string))
        else:
            execution_string = "select count(*) from {}.{} where {} >= {};".format(
                database, table, 
                key, start)
        number_of_data = pd.read_sql(execution_string, con=self.connection).iloc[0,0]
        return number_of_data

    def get_min_max(self, key, table):
        """get min and max of key"""
        warnings.warn("get_min_max is deprecated, please use SQL in original", DeprecationWarning)
        
        execution_string = "SELECT MIN({}) FROM {}".format(key, table)
        minimum = self.execute(execution_string).fetchone()[0]
        execution_string = "SELECT MAX({}) FROM {}".format(key, table)
        maximum = self.execute(execution_string).fetchone()[0]
        return minimum, maximum

    def get_last_value_before(self, ids=None,
                              time_start=None,
                              time_end=None,
                              ts_database=None,
                              ts_table=None,
                              ts_time_column=None,
                              ts_value_column=None,
                              ts_itemid_column=None,
                              ts_quality_id_column=None,
                              ts_quality_id=None,
                              not_null=True,#not used(only for copy+paste)
                              sort_by=None,
                              sort_order=None,
                              additional_sql=None):
        """
        function:       get_last_value_before
        Description:    get last value before time_start with various parameters
                        Attention: if the standard parameters are not set,
                            the function will take standard extra parameters
        ########
        Inputs
        ########
        Variable:       ids
        Description:    single or list of ids, which identify the timeseries
        Type:           int, list, dict
        ########
        Variable:       time_start
        Description:    Start time of timeseries
        Type:           str
        Example:        time_start="2015-12-20 00:00:00"
        Standard:       time_start=(dt.now()-timedelta(hours=1)).strftime(self.time_format)
        ########
        Variable:       time_end
        Description:    End time of timeseries
        Type:           str
        Example:        time_end="2015-12-21 00:00:00"
        Standard:       time_end=dt.now().strftime(self.time_format)
        
        ########
        Variable:       ts_database
        Description:    The database name to use
        Type:           str
        ########
        Variable:       ts_table
        Description:    The table name to use
        Type:           str
        ########
        Variable:       ts_time_column
        Description:    The column name of timestamp
        Type:           str
        ########
        Variable:       ts_itemid_column
        Description:    The column name of ids, which identify the timeseries
        Type:           str
        ########
        Variable:       ts_value_column
        Description:    The column name of values of timeseries
        Type:           str
        ########
        Variable:       ts_quality_id_column
        Description:    The column name of quality_id
        Type:           str
        ########
        Variable:       ts_quality_id
        Description:    The standard value of quality_id
        Type:           int,str
        ########
        Outputs
        ########
        Variable:       data
        Description:    fetched timeseries data of database query
        Type:           list
        """

        "if some parameters are not handed over, take standard arguments"

        (time_start, time_end, ts_database, ts_table, ts_time_column, ts_value_column, ts_itemid_column, _,
         ts_quality_id_column, ts_quality_id,
         time_format) = self._get_ts_standard(time_start=time_start,
                                              time_end=time_end,
                                              ts_database=ts_database,
                                              ts_table=ts_table,
                                              ts_time_column=ts_time_column,
                                              ts_value_column=ts_value_column,
                                              ts_itemid_column=ts_itemid_column,
                                              ts_chosen_key="",
                                              ts_quality_id_column=ts_quality_id_column,
                                              ts_quality_id=ts_quality_id,
                                              time_format=None)
        (ids_keys, ids_values, ids_dict) = self._handle_ids(ids)
        sort_by = self._handle_sort_by(sort_by)
        #        if sort_by == None:
        #            sort_by = self.ts_time_column
        if additional_sql is not None:
            additional_sql = "{} {}".format(additional_sql, 'LIMIT 1')
        else:
            additional_sql = " LIMIT 1"
        if type(ids_keys) == int:
            execution_string = self.__get_ts_string(ids=ids_keys,
                                                    time_start=None,
                                                    time_end=time_start,
                                                    ts_database=ts_database,
                                                    ts_table=ts_table,
                                                    ts_time_column=ts_time_column,
                                                    ts_itemid_column=ts_itemid_column,
                                                    ts_value_column=ts_value_column,
                                                    ts_quality_id_column=ts_quality_id_column,
                                                    ts_quality_id=ts_quality_id,
                                                    not_null=True,
                                                    sort_by=ts_time_column,
                                                    sort_order="DESC",
                                                    additional_sql=additional_sql)
            data = self.execute_fetchall(execution_string, ts_time_column)
        elif type(ids_keys) == list:
            data = pd.DataFrame(columns=[ts_itemid_column,
                                             ts_value_column])
            for entry in ids_keys:
                execution_string = self.__get_ts_string(ids=entry,
                                                        time_start=None,
                                                        time_end=time_start,
                                                        ts_database=ts_database,
                                                        ts_table=ts_table,
                                                        ts_time_column=ts_time_column,
                                                        ts_itemid_column=ts_itemid_column,
                                                        ts_value_column=ts_value_column,
                                                        ts_quality_id_column=ts_quality_id_column,
                                                        ts_quality_id=ts_quality_id,
                                                        not_null=True,
                                                        sort_by=ts_time_column,
                                                        sort_order="DESC",
                                                        additional_sql=additional_sql)
                temp_data = self.execute_fetchall(execution_string, ts_time_column)
                data = pd.concat([data, temp_data])

        if sort_by:
            if sort_order == None:
                sort_order = "ASC"
            if sort_order == "ASC":
                ascending = True
            elif sort_order == "DESC":
                ascending = False
            data.sort_index(ascending=ascending, inplace=True)
        return data

    """custom made odbc commands"""

    def get_timeseries(self, ids=None,
                       time_start=None,
                       time_end=None,
                       ts_database=None,
                       ts_table=None,
                       ts_time_column=None,
                       ts_itemid_column=None,
                       ts_value_column=None,
                       ts_quality_id_column=None,
                       ts_quality_id=None,
                       not_null=True,
                       sort_by=None,
                       sort_order=None,
                       additional_sql=None):
        """
        function:       get_timeseries
        Description:    get timeseries with various parameters
                        Attention: if the standard parameters are not set,
                            the function will take standard extra parameters
        ########
        Inputs
        ########
        Variable:       ids
        Description:    single or list of ids, which identify the timeseries
        Type:           int, list
        ########
        Variable:       time_start
        Description:    Start time of timeseries
        Type:           str
        Example:        time_start="2015-12-20 00:00:00"
        Standard:       time_start=(dt.now()-timedelta(hours=1)).strftime(self.time_format)
        ########
        Variable:       time_end
        Description:    End time of timeseries
        Type:           str
        Example:        time_end="2015-12-21 00:00:00"
        Standard:       time_end=dt.now().strftime(self.time_format)
        ########
        Variable:       ts_database
        Description:    The database name to use
        Type:           str
        ########
        Variable:       ts_table
        Description:    The table name to use
        Type:           str
        ########
        Variable:       ts_time_column
        Description:    The column name of timestamp
        Type:           str
        ########
        Variable:       ts_itemid_column
        Description:    The column name of ids, which identify the timeseries
        Type:           str
        ########
        Variable:       ts_value_column
        Description:    The column name of values of timeseries
        Type:           str
        ########
        Variable:       ts_quality_id_column
        Description:    The column name of quality_id
        Type:           str
        ########
        Variable:       ts_quality_id
        Description:    The standard value of quality_id
        Type:           int,str
        ########
        Outputs
        ########
        Variable:       data
        Description:    fetched timeseries data of odbc query
        Type:           list
        """

        "if some parameters are not handed over, take standard arguments"
        (time_start, time_end, ts_database, ts_table,
         ts_time_column, ts_value_column, ts_itemid_column,
         _, ts_quality_id_column, ts_quality_id,
         time_format) = self._get_ts_standard(
            time_start=time_start,
            time_end=time_end,
            ts_database=ts_database,
            ts_table=ts_table,
            ts_time_column=ts_time_column,
            ts_value_column=ts_value_column,
            ts_itemid_column=ts_itemid_column,
            ts_chosen_key="",
            ts_quality_id_column=ts_quality_id_column,
            ts_quality_id=ts_quality_id,
            time_format=None)
        (ids_keys, ids_values, ids_dict) = self._handle_ids(ids)
        sort_by = self._handle_sort_by(sort_by,
                                       ts_time_column,
                                       ts_itemid_column,
                                       ts_value_column)
        """get the string for SQL"""

        execution_string = self.__get_ts_string(ids=ids_keys,
                                                time_start=time_start,
                                                time_end=time_end,
                                                ts_database=ts_database,
                                                ts_table=ts_table,
                                                ts_time_column=ts_time_column,
                                                ts_itemid_column=ts_itemid_column,
                                                ts_value_column=ts_value_column,
                                                ts_quality_id_column=ts_quality_id_column,
                                                ts_quality_id=ts_quality_id,
                                                not_null=not_null,
                                                sort_by=sort_by,
                                                sort_order=sort_order,
                                                additional_sql=additional_sql)
        data = self.execute_fetchall(execution_string, ts_time_column)
        return data

    def get_timeseries_df(self, ids=None,
                          time_start=None,
                          time_end=None,
                          ts_database=None,
                          ts_table=None,
                          ts_time_column=None,
                          ts_itemid_column=None,
                          ts_value_column=None,
                          ts_quality_id_column=None,
                          ts_quality_id=None,
                          not_null=True,
                          sort_by=None,
                          sort_order="ASC",
                          additional_sql=None,
                          use_query=False,
                          get_last_value_before=True,
                          replace_first_index=True):
        """
        :param ids: dict, list, string, int with different ids
        :param time_start: start time of sql query
        :param time_end: end time of sql query
        :param ts_database: database to use
        :param ts_table: table to use
        :param ts_time_column: time column of timeseries table
        :param ts_itemid_column: itemid column of timeseries table
        :param ts_value_column: value column of timeseries table
        :param ts_quality_id_column: qualityid column of timeseries table
        :param ts_quality_id: chosen qualityid
        :param not_null: if chosen column != null
        :param sort_by: column which will be sorted
        :param sort_order: sort order ("ASC" or "DESC")
        :param additional_sql: additional sql parameters
        :param use_query: if query function of
        :param get_last_value_before: if get_last_value_before function will be used
        :param replace_first_index: if first index will be set to time_start with elements of get_last_value_before
        :return: data
        :rtype: pandas.DataFrame
        """
        """get standard parameters"""
        (time_start, time_end, ts_database, ts_table,
         ts_time_column, ts_value_column, ts_itemid_column,
         _, ts_quality_id_column, ts_quality_id,
         time_format) = self._get_ts_standard(
            time_start=time_start,
            time_end=time_end,
            ts_database=ts_database,
            ts_table=ts_table,
            ts_time_column=ts_time_column,
            ts_value_column=ts_value_column,
            ts_itemid_column=ts_itemid_column,
            ts_chosen_key="",
            ts_quality_id_column=ts_quality_id_column,
            ts_quality_id=ts_quality_id,
            time_format=None)

        (ids_keys, ids_values, ids_dict) = self._handle_ids(ids)
        sort_by = self._handle_sort_by(sort_by,
                                       ts_time_column,
                                       ts_itemid_column,
                                       ts_value_column)
        if use_query:
            raw_data = self.query(ids=ids_keys,
                                  time_start=time_start,
                                  time_end=time_end)
        else:
            raw_data = self.get_timeseries(ids=ids_keys,
                                           time_start=time_start,
                                           time_end=time_end,
                                           sort_by="ts_time_column",
                                           sort_order=sort_order)
        data = self._ts_to_df_matrix(raw_data, ids=ids_dict)
        if sort_order == "ASC":
            data.sort_index(ascending=True, inplace=True)
            data.fillna(method="ffill", inplace=True)
        elif sort_order == "DESC":
            data.sort_index(ascending=False, inplace=True)
            data.fillna(method="bfill", inplace=True)

        if get_last_value_before:
            if use_query:
                time_start_dt = dt.strptime(time_start, self.time_format)
                year = time_start_dt.year
                month = time_start_dt.month
                t_table = "measurement{}{:02d}".format(year, month)
                data2 = self.get_last_value_before(ids=ids_keys,
                                                   time_start=time_start,
                                                   ts_table=t_table)
                
                if sort_by:
                    if sort_order == None:
                        sort_order = "ASC"
                    if sort_order == "ASC":
                        ascending = True
                    elif sort_order == "DESC":
                        ascending = False
                    data2.sort_index(ascending=ascending, inplace=True)
            else:
                data2 = self.get_last_value_before(ids=ids_keys,
                                                   time_start=time_start)
                if sort_by:
                    if sort_order == None:
                        sort_order = "ASC"
                    if sort_order == "ASC":
                        ascending = True
                    elif sort_order == "DESC":
                        ascending = False
                    data2.sort_index(ascending=ascending, inplace=True)
            if replace_first_index:
                data2 = self.__df_set_ts_index(data2, time_start)
            data2 = self._ts_to_df_matrix(data2, ids=ids)
            data2.index = pd.to_datetime(data2.index)
            data2.columns = ids_values
            if sort_order == "ASC":
                data = pd.concat([data2, data])
                data.fillna(method="ffill", inplace=True)
            elif sort_order == "DESC":
                data = pd.concat([data, data2])
                data.fillna(method="bfill", inplace=True)
                # data.sort_index()

        return data

    def query(self, ids, time_start, time_end=None):
        """
        :param ids: dict, list, string, int with different ids, which identify the timeseries
        :param time_start: Start time of timeseries
        :param time_end: End time of timeseries
        :keyword engine: "pandas" or "odbc"
        :return data: pandas.DataFrame with queried data
        :rtype: pandas.DataFrame
        """
        """
        function:       query
        Description:    query for E.ON ERC main building with various parameters
                        Attention: the function will take standard extra parameters,
                        if not set, the function doesn't work
        ########
        Inputs
        ########
        Variable:       ids
        Description:    single or list of ids, which identify the timeseries
        Type:           int, list
        ########
        Variable:       time_start
        Description:    Start time of timeseries
        Type:           str
        Example:        time_start="2015-12-20 00:00:00"
        ########
        Variable:       time_end
        Description:    End time of timeseries
        Type:           str
        Example:        time_end="2015-12-21 00:00:00"
        ########
        Outputs
        ########
        Variable:       data
        Description:    fetched timeseries data of odbc query
        Type:           list
        """
        """get standard parameters"""
        (time_start, time_end, ts_database, ts_table, ts_time_column, ts_value_column, ts_itemid_column,
         _, ts_quality_id_column, ts_quality_id,
         time_format) = self._get_ts_standard(time_start=time_start,
                                              time_end=time_end,
                                              ts_database=None,
                                              ts_table=None,
                                              ts_time_column=None,
                                              ts_value_column=None,
                                              ts_itemid_column=None,
                                              ts_chosen_key="",
                                              ts_quality_id_column=None,
                                              ts_quality_id=None,
                                              time_format=None)
        time_start_dt = dt.strptime(time_start, self.time_format)
        if time_end is None:
            time_end_dt = dt.now()
        if time_end is not None:
            time_end_dt = dt.strptime(time_end, self.time_format)
        if time_start_dt < dt(2014, 5, 1, 0, 0, 0):
            warnings.warn("Start Time must be later than 2014-05-01, changed automatically to 2014-05-01!",
                          RuntimeWarning)
            time_start_dt = dt(2014, 5, 1, 0, 0, 0)
        data = pd.DataFrame(columns=[ts_itemid_column,
                                         ts_value_column])
        start_year = time_start_dt.year
        end_year = time_end_dt.year
        for year in range(start_year, end_year + 1):
            # print(str(year))
            temp_month_start = 1
            temp_month_end = 12
            if year == start_year:
                temp_month_start = time_start_dt.month
            if year == end_year:
                temp_month_end = time_end_dt.month
            for month in range(temp_month_start, temp_month_end + 1):
                t_table = "measurement{}{:02d}".format(year, month)
                temp_data = self.get_timeseries(ids=ids,
                                                time_start=time_start,
                                                time_end=time_end,
                                                ts_database=ts_database,
                                                ts_table=t_table,
                                                ts_time_column=ts_time_column,
                                                ts_itemid_column=ts_itemid_column,
                                                ts_value_column=ts_value_column,
                                                ts_quality_id_column=ts_quality_id_column,
                                                ts_quality_id=ts_quality_id,
                                                not_null=True,
                                                sort_by="ts_time_column",
                                                sort_order="ASC")
                data = pd.concat([data, temp_data])
        if time_end_dt.date() >= dt.today().date():
            t_table = "measurement"
            temp_data = self.get_timeseries(ids=ids,
                                            time_start=time_start,
                                            time_end=time_end,
                                            ts_database=ts_database,
                                            ts_table=t_table,
                                            ts_time_column=ts_time_column,
                                            ts_itemid_column=ts_itemid_column,
                                            ts_value_column=ts_value_column,
                                            ts_quality_id_column=ts_quality_id_column,
                                            ts_quality_id=ts_quality_id,
                                            not_null=True,
                                            sort_by="ts_time_column",
                                            sort_order="ASC")

            data = pd.concat([data, temp_data])
        return data

    """get items from item table"""

    def get_itemid(self, search_item,
                   item_database=None,
                   item_table=None,
                   item_itemid_column=None,
                   item_itemname_column=None,
                   additional_sql=None,
                   encoding="UTF-8"):
        """
        function:       get_itemid
        Description:    get itemid with various parameters
                        Attention: if the parameters are not set,
                            the function will take standard parameters
        ########
        Inputs
        ########
        Variable:       search_item
        Description:    The search item, which will be searched in item-table
        Type:           str,list
        ########
        Variable:       database
        Description:    The database name to use
        Type:           str
        ########
        Variable:       table
        Description:    The table name to use
        Type:           str
        ########
        Variable:       itemid_column
        Description:    The column name of itemids, which identify the timeseries
        Type:           str
        ########
        Variable:       itemname_column
        Description:    The column name of itemnames of timeseries
        Type:           str
        ########
        Variable:       engine
        Description:    engine of executing and fetching
        Type:           str
        Examples:       'odbc': standard odbc engine
                        'pandas': engine of pandas for compability with pandas
        ########
        Outputs
        ########
        Variable:       data
        Description:    fetched item data of odbc query
        Type:           list
        ########
        """

        """if some parameters are not handed over, take standard arguments"""
        (item_database, item_table, item_itemid_column,
         item_itemname_column) = self._get_item_standard(
            item_database, item_table,
            item_itemid_column, item_itemname_column)
        """check allowed types"""
        if isinstance(search_item, list) and self.__check_list_str(search_item):
            execution_string = 'SELECT {},{} FROM `{}` WHERE '.format(
                item_itemid_column, item_itemname_column,
                item_table)
            item_i = 0
            for item in search_item:
                if item_i > 0:
                    execution_string = "{} OR `{}` LIKE '%%{}%%'".format(
                        execution_string, item_itemname_column, item)
                else:
                    execution_string = "{}`{}` LIKE '%%{}%%'".format(
                        execution_string, item_itemname_column, item)
                item_i += 1
            execution_string = "{} ORDER BY {}".format(execution_string,
                                                       item_itemid_column)
        elif isinstance(search_item, str):
            execution_string = """SELECT {},{} FROM `{}`
                            WHERE `{}` LIKE '%%{}%%' ORDER BY {}""".format(
                item_itemid_column,
                item_itemname_column,
                item_table,
                item_itemname_column,
                search_item,
                item_itemid_column)
        else:
            raise TypeError("incorrect type, string (str) or string (str) list needed")
        if additional_sql is not None:
            execution_string += additional_sql
        temp_data = self.execute_fetchall(execution_string, index_col=item_itemid_column)


        if (temp_data[item_itemname_column].dtype is bytearray):
                temp_data[item_itemname_column] = temp_data[item_itemname_column].str.decode(encoding)
        data = temp_data
        return data

    def get_itemname(self, search_item,
                     item_database=None,
                     item_table=None,
                     item_itemid_column=None,
                     item_itemname_column=None,
                     additional_sql=None,
                     encoding="UTF-8"):
        """
        function:       get_itemname
        Description:    get itemname with various parameters
                        Attention: if the parameters are not set,
                            the function will take standard extra parameters
        ########
        Inputs
        ########
        Variable:       search_item
        Description:    The search item, which will be searched in item-table
        Type:           int,list
        ########
        Variable:       item_database
        Description:    The database name to use
        Type:           str
        ########
        Variable:       item_table
        Description:    The table name to use
        Type:           str
        ########
        Variable:       item_itemid_column
        Description:    The column name of itemids, which identify the timeseries
        Type:           str
        ########
        Variable:       item_itemname_column
        Description:    The column name of itemnames of timeseries
        Type:           str
        ########
        Variable:       encoding
        Description:    encoding for itemname column
        Type:           str
        Examples:       'UTF-8' for UTF-8 encoding
        ########
        Outputs
        ########
        Variable:       data
        Description:    fetched item data as table of odbc query
        Type:           list
        ########
        """

        """if some parameters are not handed over, take standard arguments"""
        (item_database, item_table, item_itemid_column,
         item_itemname_column) = self._get_item_standard(
            item_database, item_table,
            item_itemid_column, item_itemname_column)
        """check allowed types"""
        if isinstance(search_item, list):
            if self.__check_list_int(search_item):
                execution_string = 'SELECT {},{} FROM `{}` WHERE `{}` in ({}) ORDER BY {}'.format(
                    item_itemid_column, item_itemname_column,
                    item_table,
                    item_itemid_column,
                    self.__list_into_str(search_item),
                    item_itemid_column)
            else:
                raise TypeError("incorrect type, integer (int) list needed")
        elif isinstance(search_item, int):
            execution_string = "SELECT {},{} FROM `{}` WHERE `{}` LIKE %%{}%% ORDER BY {}".format(
                item_itemid_column, item_itemname_column,
                item_table,
                item_itemid_column, search_item,
                item_itemid_column)
        else:
            raise TypeError("incorrect type, integer (int) or integer (int) list needed")
        if additional_sql is not None:
            execution_string += additional_sql
        temp_data = self.execute_fetchall(execution_string, index_col=item_itemid_column)

        if (temp_data[item_itemname_column].dtype is bytearray):
                temp_data[item_itemname_column] = temp_data[item_itemname_column].str.decode(encoding)
        data = temp_data
        return data

    def checkID(self, search_item,
                item_database=None,
                item_table=None,
                item_itemid_column=None,
                item_itemname_column=None,
                additional_sql=None):
        """see check_id"""
        warnings.warn("outdated: use function check_id instead", DeprecationWarning)
        self.check_id(self, search_item, item_database, item_table, item_itemid_column,
                      item_itemname_column, additional_sql)

    def check_id(self, search_item,
                 item_database=None,
                 item_table=None,
                 item_itemid_column=None,
                 item_itemname_column=None,
                 additional_sql=None):
        """
        function:       checkID
        Description:    get itemid and itemname with various parameters
                        Attention: if the standard parameters are not set,
                            the function will take standard extra parameters
        ########
        Inputs
        ########
        Variable:       search_item
        Description:    The search item, which will be searched in item-table
        Type:           str,int,list
        ########
        Variable:       database
        Description:    The database name to use
        Type:           str
        ########
        Variable:       table
        Description:    The table name to use
        Type:           str
        ########
        Variable:       itemid_column
        Description:    The column name of itemids, which identify the timeseries
        Type:           str
        ########
        Variable:       itemname_column
        Description:    The column name of itemnames of timeseries
        Type:           str
        ########
        Variable:       engine
        Description:    engine of executing and fetching
        Type:           str
        Examples:       'odbc': standard odbc engine
                        'pandas': engine of pandas for compability with pandas
        ########
        Variable:       encoding
        Description:    encoding for itemname column
        Type:           str
        Examples:       'UTF-8' for UTF-8 encoding
        ########
        Outputs
        ########
        Variable:       data
        Description:    fetched item data as table of odbc query
        Type:           list
        ########
        """

        "if some parameters are not handed over, take standard arguments"
        (item_database, item_table, item_itemid_column,
         item_itemname_column) = self._get_item_standard(
            item_database, item_table,
            item_itemid_column, item_itemname_column)

        "input type handling"
        if isinstance(search_item, str):
            data = self.get_itemid(search_item,
                                   item_database,
                                   item_table,
                                   item_itemid_column,
                                   item_itemname_column,
                                   additional_sql)
        elif isinstance(search_item, int):
            data = self.get_itemname(search_item,
                                     item_database,
                                     item_table,
                                     item_itemid_column,
                                     item_itemname_column,
                                     additional_sql)
        elif isinstance(search_item, list) and (
                    self.__check_list_str(search_item) or
                    self.__check_list_int(search_item)):
            if self.__check_list_str(search_item):
                data = self.get_itemid(search_item,
                                       item_database,
                                       item_table,
                                       item_itemid_column,
                                       item_itemname_column,
                                       additional_sql)
            elif self.__check_list_int(search_item):
                data = self.get_itemname(search_item,
                                         item_database, item_table,
                                         item_itemid_column,
                                         item_itemname_column,
                                         additional_sql)
        
        else:
            raise TypeError("""incorrect type, integer (int),
                            integer (int) list, string(str)
                            or string (str) list needed""")
        # for row in data:
        #            type_fixed_row = tuple([el.decode('utf-8') if type(el) is bytearray else el for el in row])
        #            #print( type_fixed_row )
        return data
        
    def check_id_od(self, search_item):
        """
        ###ATTENTION: HARD CODED###
        function:       check_id_od
        Description:    get itemid and itemname with various parameters
                        Attention: if the standard parameters are not set,
                            the function will take standard extra parameters
        ########
        Inputs
        ########
        Variable:       search_item
        Description:    The search item, which will be searched in item-table
        Type:           str,int,list
        ########
        Outputs
        ########
        Variable:       data_od
        Description:    fetched item data as ordered_dict
        Type:           OrderedDict
        ########
        """
        item_table = self.check_id(search_item=search_item)
        data_od=OrderedDict(item_table[self.item_itemname_column])
        for element in search_item:
            data_od.move_to_end(element)
        return data_od
        
    """support functions"""

    def __check_list_str(self, lst):
        """
        function:       __check_list_str
        Description:    check if all items in list are consequently str
        ########
        Inputs
        ########
        Variable:       lst
        Description:    The list, which will be analyzed
        Type:           list
        ########
        Outputs
        ########
        Description:    boolean if all items in list are consequently str
        Type:           bool
        ########
        """
        return bool(lst) and not isinstance(lst, str) and all(isinstance(elem, str) for elem in lst)

    def __check_list_int(self, lst):
        """
        function:       __check_list_int
        Description:    check if all items in list are consequently int
        ########
        Inputs
        ########
        Variable:       lst
        Description:    The list, which will be analyzed
        Type:           list
        ########
        Outputs
        ########
        Description:    boolean if all items in list are consequently int
        Type:           bool
        ########
        """
        return bool(lst) and not isinstance(lst, int) and all(isinstance(elem, int) for elem in lst)

    def __list_into_str(self, lst, separator=', '):
        """
        function:       __list_into_str
        Description:    merge list into one single string with seperator
                        between elements of list
        ########
        Inputs
        ########
        Variable:       lst
        Description:    The list, which will be merged
        Type:           list
        ########
        Variable:       separator
        Description:    separator, which will be set between all elements of lst
        Type:           str
        ########
        Outputs
        ########
        Description:    merged list with all elements of lst in it
        Type:           str
        ########
        """
        return separator.join(str(x) for x in lst)

    def __df_set_ts_index(self, dataframe, new_index):
        """
        set new index in dataframe
        :param dataframe: pandas.DataFrame, which will be changed
        :param new_index: new index, which will be set
        :return dataframe: changed pandas.DataFrame
        """
        new_index = dt.strptime(new_index, self.time_format)
        new_index = [new_index] * len(dataframe.index)
        new_index = pd.DatetimeIndex(new_index)
        dataframe.set_index(new_index, inplace=True)
        return dataframe

    """handle ids with different types"""

    def _handle_ids(self, ids):
        """
        :param ids: ids, which will be handled
        :type ids: dict, collections.OrderedDict, list, str, int
        :return: (ids_keys, ids_values, ids_dict)
        :rtype: (list, list, dict)
        """
        if type(ids) is dict:
            ids_keys = list(ids.keys())
            ids_values = list(ids.values())
            ids_dict = ids
        elif "OrderedDict" in type(ids).__name__:
            ids_keys = list(ids.keys())
            ids_values = list(ids.values())
            ids_dict = ids
        elif type(ids) is list:
            ids_keys = ids
            ids_values = ids
            ids_dict = dict((k, k) for k in ids)
            """fst: ids_dict has to be considered"""
        elif type(ids) is int:
            ids_keys = ids
            ids_values = ids
            ids_dict = {ids: ids}
        elif ids is None:
            ids_keys = None
            ids_values = None
            ids_dict = {None: None}
            warnings.warn("type of ids is None", RuntimeWarning)
        else:
            raise Exception("Programming", """type of ids is not dict,OrderedDict, list or int,
                                            but {}""".format(type(ids)))
        return (ids_keys, ids_values, ids_dict)

    """handle sort_by with standard parameters"""

    def _handle_sort_by(self, sort_by,
                        ts_time_column=None,
                        ts_itemid_column=None,
                        ts_value_column=None):
        """

        :param sort_by: handled sort_by parameter (str)
        :param ts_time_column: str
        :param ts_itemid_column: str
        :param ts_value_column: str
        :return sort_by: str
        """
        if ts_time_column is None:
            ts_time_column = self.ts_time_column
        if ts_itemid_column is None:
            ts_itemid_column = self.ts_itemid_column
        if ts_value_column is None:
            ts_value_column = self.ts_value_column
        if sort_by is None:
            sort_by = ts_time_column
        elif sort_by == "ts_time_column":
            sort_by = ts_time_column
        elif sort_by == "ts_itemid_column":
            sort_by = ts_itemid_column
        elif sort_by == "ts_value_column":
            sort_by = ts_value_column
        return sort_by

    def __get_ts_string(self, ids,
                        time_start,
                        time_end,
                        ts_database,
                        ts_table,
                        ts_time_column,
                        ts_itemid_column,
                        ts_value_column,
                        ts_quality_id_column=None,
                        ts_quality_id=None,
                        not_null=True,
                        sort_by=None,
                        sort_order=None,
                        additional_sql=None):
        """
        function:       __get_ts_string
        Description:    get string for timeseries retrieve
        ########
        Inputs
        ########
        Variable:       dataframe
        Description:    input dataframe from get_timeseries
        Type:           pandas.core.frame.DataFrame
        Example:        columns [timestamp,ids,value]
        ########
        Variable:       ids
        Description:    dict or list of ids, key:id, value:label
        Type:           dict[int,str] or list[int]
        Explanation:    if list, then key=value
                        if ids=None, ids will be extracted from ts_itemid_column
        ########
        Variable:       ts_itemid_column
        Description:    column name of itemids
        Type:           str
        ########
        Outputs
        ########
        Variable:       data
        Description:    output dataframe
        Type:           pandas.core.frame.DataFrame
        ########
        """
        """get the string for SQL"""
        execution_string = 'SELECT {},{},{} FROM {}.{}'.format(
            ts_time_column, ts_itemid_column, ts_value_column,
            ts_database, ts_table)

        """set string for time values"""
        if time_start is not None and time_end is not None:
            execution_string = '{} WHERE {}>="{}" and {}<"{}"'.format(execution_string,
                                                                      ts_time_column,
                                                                      time_start,
                                                                      ts_time_column,
                                                                      time_end)
        elif time_start is not None and time_end is None:
            execution_string = '{} WHERE {}>="{}" '.format(execution_string,
                                                           ts_time_column,
                                                           time_start)
        elif time_start is None and time_end is not None:
            execution_string = '{} WHERE {}<"{}" '.format(execution_string,
                                                          ts_time_column,
                                                          time_end)
        """add handling for ids"""
        if ids is not None:
            if type(ids) is list:
                execution_string += 'and {} in ({})'.format(ts_itemid_column,
                                                            self.__list_into_str(ids))
            else:
                execution_string += 'and {} = {}'.format(ts_itemid_column, ids)

        # print(execution_string)
        """add quality id query"""
        if ts_quality_id_column is not None:
            execution_string = "{} and {} in ({})".format(execution_string,
                                                          ts_quality_id_column,
                                                          ts_quality_id)
        """add if time column not null"""
        if not_null:
            execution_string = "{} AND `{}` IS NOT NULL".format(execution_string,
                                                                ts_time_column)
        """add if column will be sort"""
        if sort_by:
            sort_by = self._handle_sort_by(sort_by,
                                           ts_time_column=ts_time_column,
                                           ts_itemid_column=ts_itemid_column,
                                           ts_value_column=ts_value_column)

            execution_string = "{} ORDER BY `{}`".format(execution_string, sort_by)
            if sort_order:
                execution_string = "{} {}".format(execution_string, sort_order)
        if additional_sql:
            execution_string = "{} {}".format(execution_string, additional_sql)
        return execution_string

    def _ts_to_df_matrix(self, dataframe, 
                         ids=None, 
                         ts_itemid_column=None,
                         delete_duplicates=True,
                         keep="first",
                         sort_index=True,
                         sort_order="ASC",
                         fillna=True):
        """
        function:       _ts_to_df_matrix
        Description:    transform timeseries into pandas.dataframe matrix
                        with ts_itemid_column as index
        ########
        Inputs
        ########
        Variable:       dataframe
        Description:    input dataframe from get_timeseries
        Type:           pandas.core.frame.DataFrame
        Example:        columns [timestamp,ids,value]
        ########
        Variable:       ids
        Description:    dict or list of ids, key:id, value:label
        Type:           dict[int,str] or list[int]
        Explanation:    if list, then key=value
                        if ids=None, ids will be extracted from ts_itemid_column
        ########
        Variable:       ts_itemid_column
        Description:    column name of itemids
        Type:           str
        ########
        Outputs
        ########
        Variable:       data
        Description:    output dataframe
        Type:           pandas.core.frame.DataFrame
        ########
        """
        if ts_itemid_column == None:
            ts_itemid_column = self.ts_itemid_column
        """handle ids"""
        if ids == None:
            raw_ids = dataframe[ts_itemid_column].tolist()
            raw_ids = list(set(raw_ids))
            ids = {key: key for key in raw_ids}
        (_, _, ids_dict) = self._handle_ids(ids)
        """start transformation"""
        dataframe.columns = ['item_id', 'value']
        dataframe.index.name = "timestamp"
        data = pd.DataFrame(index=dataframe.index.values)#,columns=ids_dict.values())
        data = data.loc[~data.index.duplicated(keep='first')]
        for key, value in ids_dict.items():
            selected_data = dataframe.where(dataframe['item_id'] == key, np.NaN)
            selected_data = selected_data.dropna(axis=0)
            selected_data.columns = ['item_id', value]
            selected_data = selected_data[value]
            if(delete_duplicates):
                selected_data = selected_data[~selected_data.index.duplicated(keep='first')]
            data=pd.concat([data,selected_data],axis=1)
        
        if(sort_index==True):
            if sort_order=="ASC":
                ascending=True
            elif sort_order=="DESC":
                ascending=False
            data.sort_index(ascending=ascending)
        if(fillna):
            data.fillna(method="ffill",inplace=True)
        if(delete_duplicates):
            data = data[~data.index.duplicated(keep=keep)]
        return data
        
    def _get_ts_timedist(self, data, time_start, time_end, freq="1min"):
        """
        get dataframe with equidistant pandas.Datetimeindex
        :param data: pandas.DataFrame
        :param time_start: start time of wished dataframe
        :param time_end: end time of wished dataframe
        :param freq: frequency of equidistant timestamps
        :return:
        """
        time_start_dt = dt.strptime(time_start, "%Y-%m-%d %H:%M:%S")
        time_end_dt = dt.strptime(time_end, "%Y-%m-%d %H:%M:%S")


        date_range = pd.date_range(start=time_start_dt, end=time_end_dt, freq=freq)
        data_new = pd.DataFrame(index=date_range)
        for element in list(data.columns.values):
            data_new[element]=data[element].resample(freq).mean()
        data_new.fillna(method="ffill", inplace=True)
        return data_new
        
if __name__ is "__main__":
    """EXAMPLE"""
    path_to_config = "D:\Sciebo\Programmierung\GIT\EBC_Database\Settings\settings_standard.ini"
    option_groups = "odbc"
    connection = EbcSql(option_files=path_to_config,
                                    option_groups="odbc")
    connection.set_standard(option_files=path_to_config,
                            option_groups=["timeseries", "format"])
    
    
    
    
    
    print("start examples")
    """examples for different possibilities for input of ids"""
    ids_int = 1689
    ids_list = [1689, 1690, 1691]
    ids_dict = {1689: "dp1", 1690: "dp2", 1691: "dp3"}
    #from collections import OrderedDict
    ids_ordered_dict = OrderedDict([(1689, "datapoint 1"), (1690, "datapoint 2"), (1691, "datapoint 3")])

    
    """examples for different kinds of search_items for check_id, get_itemid or get_itemname"""
    search_item_string = ["CCA", "_L01", "H03"]
    search_item_int = [1689, 1690, 1691]
    search_item_single = "CCA"

    
    
    """different times"""
    time_start_short = "2016-12-31 23:00:00"
    time_end_short = "2017-01-01 01:00:00"

    time_start_long = "2015-12-27 00:00:00"
    time_end_long = "2016-01-03 00:00:00"

    time_start_day = "2016-12-31 12:00:00"
    time_end_day = "2017-01-01 12:00:00"

    time_start_ts = "2017-05-15 12:00:00"
    time_end_ts = "2017-05-16 12:00:00"
    
    
    item_table=connection.get_itemid(search_item=["CCA","_L01"])
    item_table_dict=dict(item_table)
    item_table_pandas1 = connection.get_itemid(search_item=search_item_string)
    item_table_pandas_dict=item_table_pandas1.to_dict()[connection.item_itemname_column]

#    data_query_1=connection.query(ids=search_item_int,
#                                  time_start=time_start_short,
#                                  time_end=time_end_short)
    data = connection.get_timeseries_df(ids=search_item_int,
                                    time_start=time_start_ts,
                                    time_end=time_end_ts,
                                    sort_by="ts_time_column",
                                    sort_order="ASC",
                                    use_query=True,
                                    get_last_value_before=True,
                                    replace_first_index=True)
    
    
    
    data_tw=np.average(data.y - data.x, weights=data.index.asi8)








    #item_table_pandas_dict=item_table_pandas_dict
    
    
    
#    
#
#    """example for query function of E.ON ERC main building"""
#    data_query_1=connection.query(ids=None,time_start="2016-12-20 00:00:00",time_end="2016-12-20 01:00:00")
#    data_query_2=connection.query(ids=[15,16,17],time_start="2015-12-20 00:00:00",time_end="2016-02-21 00:00:00")
#
#    """example to get itemid from itemname"""
#    item_table=connection.get_itemid(search_item=["CCA","_L01"])
#
#    """example to get itemname from itemid"""
#    item_table2=connection.get_itemname(search_item=[1211,1222])
#    """set dict for datapoints, id:name of column in df matrix"""
#    dict_ids = OrderedDict([(1689, "datapoint 1"), (1690, "datapoint 2"), (1691, "datapoint 3")])
#
#    
#    """example for get_timeseries, which will search in one mono data table"""
#    raw_data=connection.get_timeseries(ids=dict_ids,
#                                        time_start="2017-5-10 00:00:00",
#                                        time_end="2017-5-10 19:00:00",
#                                        sort_by="ts_time_column",
#                                        sort_order="ASC")
#    
#    """get the last value before time_start"""
#    data_glbv1=connection.get_last_value_before(ids=dict_ids,
#                                          time_start="2017-5-11 00:00:00")
#    
#    data_glvb2=connection.get_last_value_before(ids=dict_ids,
#                                               time_start="2017-5-11 00:00:00")
#
#    """transfer the timeseries data into a matrix"""
#    data_df=connection._ts_to_df_matrix(raw_data,ids=dict_ids)
#
#    time_start = "2017-5-11 00:00:00"
#    time_end = "2017-5-12 00:00:00"
#    
#    """get_timeseries into matrix (_ts_to_df_matrix)"""
#    data_df1 = connection.get_timeseries_df(ids=dict_ids,
#                                            time_start=time_start,
#                                            time_end=time_end,
#                                            sort_by="ts_time_column",
#                                            sort_order="ASC")
#    data_df2 = connection.get_timeseries_df(ids=dict_ids,
#                                            time_start=time_start,
#                                            time_end=time_end,
#                                            sort_by="ts_time_column",
#                                            sort_order="ASC")
#    """get_timeseries with query function for E.ON ERC main building"""
#    data_df4 = connection.get_timeseries_df(ids=ids_list,
#                                            time_start=time_start_ts,
#                                            time_end=time_end_ts,
#                                            sort_by="ts_time_column",
#                                            sort_order="DESC",
#                                            use_query=True,
#                                            get_last_value_before=True,
#                                            replace_first_index=True)
#    """get_timeseries with query function for E.ON ERC main building"""
#    data_df6 = connection.get_timeseries_df(ids=ids_list,
#                                            time_start=time_start_long,
#                                            time_end=time_end_long,
#                                            sort_by="ts_time_column",
#                                            sort_order="ASC",
#                                            use_query=True,
#                                            get_last_value_before=True,
#                                            replace_first_index=True)
#    
#    #data_df2_1min = connection._get_ts_timedist(data_df2, time_start, time_end, freq="1min")
#    data_df2_15min = connection._get_ts_timedist(data_df2, time_start, time_end, freq="15min")
#
#    dict_ids = OrderedDict([(1737, "Vflow"), (1689, "Tin"), (1690, "Tout")])
#    data_df3 = connection.get_timeseries_df(ids=dict_ids,
#                                            time_start=time_start,
#                                            time_end=time_end,
#                                            sort_by="ts_time_column",
#                                            sort_order="ASC")
#
#    """get dataframe with equidistant indexed dataframe"""
#    data_df3_1min = connection._get_ts_timedist(data_df3, time_start, time_end, freq="1min")
#    data_df3_15min = connection._get_ts_timedist(data_df3, time_start, time_end, freq="15min")
#    
#    data_df5 = connection.get_timeseries_df(ids=ids_list,
#                                            time_start=time_start_ts,
#                                            time_end=time_end_ts,
#                                            sort_by="ts_time_column",
#                                            sort_order="DESC",
#                                            use_query=False,
#                                            get_last_value_before=True,
#                                            replace_first_index=True)
    
    
    
    
    
    
