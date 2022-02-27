import pandas as pd

class data_analysis_v2:
    def __init__(self,
                 df):
        self.df = df.copy()
        self.datatypes()
        self.summary()
        self.column_summary()
        self.columns=list(self.df.columns)

    def datatypes(self):
        self.int_df = self.df.select_dtypes(include='int64')
        self.float_df = self.df.select_dtypes(include='float64')
        self.str_df = self.df.select_dtypes(include='object')
        self.bool_df = self.df.select_dtypes(include='bool')
        self.datetime_df = self.df.select_dtypes(include='datetime64')

    def summary(self):
        self.column_count = len(self.df.columns)
        self.row_count = len(self.df)
        self.row_count_commas = f'{self.row_count:,}'
        self.dtype_column_count = {'Integer':len(self.int_df.columns),
                                   'Floating Point' :len(self.float_df.columns),
                                   'String':len(self.str_df.columns),
                                   'Boolean':len(self.bool_df.columns),
                                   'Datetime':len(self.datetime_df.columns)}
        self.dtype_column_count={k: v for k, v in reversed(sorted(self.dtype_column_count.items(), key=lambda item: item[1]))}
        self.total_cells = self.column_count * self.row_count
        self.total_cells_commas = f'{self.total_cells:,}'
        self.missing_count=self.df.isnull().sum().sum()
        self.missing_count_commas = f'{self.missing_count:,}'
        self.missing_ratio = round(self.missing_count * 100 / self.total_cells,2)
        self.missing_from_integer_cols=self.int_df.isnull().sum().sum()
        self.missing_ratio_integer_cols = round(self.missing_from_integer_cols * 100 / self.total_cells,2)
        self.missing_from_float_cols = self.float_df.isnull().sum().sum()
        self.missing_ratio_float_cols = round(self.missing_from_float_cols * 100 / self.total_cells, 2)
        self.missing_from_str_cols = self.str_df.isnull().sum().sum()
        self.missing_ratio_str_cols = round(self.missing_from_str_cols * 100 / self.total_cells, 2)
        self.missing_from_bool_cols = self.bool_df.isnull().sum().sum()
        self.missing_ratio_bool_cols = round(self.missing_from_bool_cols * 100 / self.total_cells, 2)
        self.missing_from_datetime_cols = self.datetime_df.isnull().sum().sum()
        self.missing_ratio_datetime_cols = round(self.missing_from_datetime_cols * 100 / self.total_cells, 2)

    def column_summary(self):
        self.col_sum = pd.DataFrame(columns=['Number','Column','Datatype','Count','Unique Values',
                                             'Missing Values','Missing Values Contribution%','Cardinality%','Cardinality Level'])
        for i,col in enumerate(self.df.columns):
            dt= self.df.dtypes[col]
            count= len(self.df[col])
            unique= self.df[col].nunique()
            missing= self.df[col].isnull().sum()
            missing_contribution = round(missing*100/self.missing_count,2)
            cardinality= round(unique*100/(count-missing),2)
            cardinality_bin = "Very Low" if cardinality <= 15 else "Low" if cardinality <= 30 \
                else "Medium" if cardinality <= 50 else "High" if cardinality <= 75 \
                else "Very High"
            self.col_sum.loc[i] = [i+1,col,dt,count,unique,missing,missing_contribution,cardinality,cardinality_bin ]
        self.col_sum_nrow = len(self.col_sum)
        self.col_sum_ncol = len(self.col_sum.columns)

    def column_info(self,col):
        return self.col_sum[self.col_sum['Column']==col]

    def numeric_column(self,col):
        column = self.df[col]
        num_dt = {'int64':'Integer','float64':'Floating-point'}
        dt=num_dt[str(column.dtypes)]
        max_=f'{round(column.max(),2):,}' if dt=='Floating-point' else f'{column.max():,}'
        min_=f'{round(column.min(),2):,}' if dt=='Floating-point' else f'{column.min():,}'
        mean_=f'{round(column.mean(),2):,}'
        q25=f'{round(column.quantile(0.25),2):,}'
        q50=round(column.quantile(0.5),2)
        q75=round(column.quantile(0.75),2)
        skew=round(column.skew(),2)
        return {'dt':dt,'max':max_,'min':min_,'mean':mean_,'q25':q25,'q50':q50,'q75':q75,'skew':skew}

    def str_col(self,col):
        column = self.df[col].dropna()
        str_dt="String"
        words = []
        for row in range(len(column)):
            text_list = column.iloc[row].split()
            for t in text_list:
                words.append(t.strip())
        top_n_words = pd.Series(words).value_counts().head().reset_index().rename(columns = {"index": "string", 0: "count"})
        top_n_words['perc'] = top_n_words['string'].apply(lambda x: sum([1 if x == i else 0 for i in words]) * 100/ len(words)).round(2)

        top_values = column.value_counts().head().reset_index()
        top_values.columns=["value","count"]
        top_values['value'] = top_values['value'].apply(lambda x: x[:20]+"..." if len(x)>20 else x)
        top_values['perc_value']= (top_values['count']*100/self.row_count).round(2)



        return {'top_n_words':top_n_words,'length':len(top_n_words),'words': f'{len(words):,}','words_dist' : f'{len(set(words)):,}',
                'top_values':top_values,'length_2':len(top_values)}


    def histogram_data(self,col):
        column = pd.DataFrame(self.df[col]).dropna()
        column['bin'] = pd.cut(column[col], 10)
        column['upper']=column['bin'].apply(lambda y: y.right)
        tab = column['upper'].value_counts().reset_index().sort_values(by='index').reset_index(drop=True)
        count_dict = list(reversed(sorted(list(tab["upper"].unique()))))
        count_length_map=    {1:['bg-red-700'],
             2:['bg-red-900','bg-red-50'],
             3:['bg-red-900','bg-red-500','bg-red-50'],
             4:['bg-red-900','bg-red-700','bg-red-300','bg-red-50'],
             5:['bg-red-900','bg-red-700','bg-red-500','bg-red-300','bg-red-50'],
             6:['bg-red-900', 'bg-red-800', 'bg-red-600', 'bg-red-400','bg-red-200','bg-red-50'],
             7:['bg-red-900', 'bg-red-800', 'bg-red-600', 'bg-red-500','bg-red-400', 'bg-red-200','bg-red-50'],
             8:['bg-red-900', 'bg-red-800', 'bg-red-700','bg-red-600', 'bg-red-500', 'bg-red-400', 'bg-red-200', 'bg-red-50'],
             9:['bg-red-900', 'bg-red-800', 'bg-red-700', 'bg-red-600', 'bg-red-500', 'bg-red-400','bg-red-300', 'bg-red-200', 'bg-red-50'],
             10:['bg-red-900', 'bg-red-800', 'bg-red-700', 'bg-red-600', 'bg-red-500', 'bg-red-400', 'bg-red-300', 'bg-red-200','bg-red-100','bg-red-50']
             }
        f={}
        for i, j in zip(count_dict, count_length_map[len(count_dict)]):
            f[i] = j
        tab['color']=tab['upper'].map(f)
        return tab
























