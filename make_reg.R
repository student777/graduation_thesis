setwd('/Users/yee/workspace/econ/out/dataframe/')

simple_reg <- function(month, housing_type){
	file_name <- paste('price_', housing_type, '_', month, '.csv', sep='')
	df <- read.csv(file_name)
	fit <- lm(price ~ area + year_built, data=df)
	print(housing_type)
	summary(fit)	
}

# simple_reg('201701', 'apartment_rent')
# simple_reg('201701', 'apartment_trade')
# simple_reg('201701', 'multi_trade')
# simple_reg('201701', 'multi_rent')
# simple_reg('201701', 'multi_trade')
# simple_reg('201701', 'officetel_rent')
# simple_reg('201701', 'officetel_trade')
# simple_reg('201701', 'single_rent')
# simple_reg('201701', 'single_trade')

grid_reg <- function(month, housing_type){
	file_name <- paste('price_', housing_type, '_grid_', month, '.csv', sep='')
	df <- read.csv(file_name)
	fit <- lm(price ~ traffic + area + year_built, data=df)
	print(housing_type)
	summary(fit)	
}

grid_reg('201701', 'apartment_rent')
grid_reg('201701', 'apartment_trade')
grid_reg('201701', 'multi_trade')
grid_reg('201701', 'multi_rent')
grid_reg('201701', 'multi_trade')
grid_reg('201701', 'officetel_rent')
grid_reg('201701', 'officetel_trade')
grid_reg('201701', 'single_rent')
grid_reg('201701', 'single_trade')
