if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):
    ext_data = data[['lastupdatedat', 'flightdirection','flightname','id','mainflight',
                'scheduledatetime', 'scheduledate', 'servicetype', 'publicflightstate_flightstates',
                'route_destinations','aircrafttype_iatasub']]
    # print(ext_data.info())
    return ext_data
    
    

