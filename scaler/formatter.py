def format(num, suffix):
    prefix = [
        [1e30,'quetta'],
        [1e27,'ronna'],
        [1e24,'yotta'],
        [1e21,'zetta'],
        [1e18,'exa'],
        [1e15,'peta'],
        [1e12,'tera'],
        [1e9,'giga'],
        [1e6,'mega'],
        [1000,'kilo'],
        [1,''],
        [0.1,'deci'],
        [0.01,'centi'],
        [1e-3,'milli'],
        [1e-6,'micro'],
        [1e-9,'nano'],
        [1e-12,'pico'],
        [1e-15,'atto'],
        [1e-18,'femto'],
        [1e-21,'zepto'],
        [1e-24,'yocto'],
        [1e-27,'ronto'],
        [1e-30,'quecto']
    ]
    selected = ''
    for val in prefix:
        if val[0] <= num:
            selected = val[1]
            amount = round(num/val[0],2)
            if amount == 1:
                return f'{amount} {selected}{suffix}'
            else:
                return f'{amount} {selected}{suffix}s'