setwd('/Users/yee/workspace/econ/out/dataframe/')

simple_reg <- function(month, housing_type){
	file_name <- paste('price_', housing_type, '_', month, '.csv', sep='')
	df <- read.csv(file_name)
	fit <- lm(price ~ area + year_built, data=df)
	print(housing_type)
	summary(fit)	
}

simple_reg('201701', 'apartment_rent')
simple_reg('201701', 'apartment_trade')
simple_reg('201701', 'multi_trade')
simple_reg('201701', 'multi_rent')
simple_reg('201701', 'multi_trade')
simple_reg('201701', 'officetel_rent')
simple_reg('201701', 'officetel_trade')
simple_reg('201701', 'single_rent')
simple_reg('201701', 'single_trade')