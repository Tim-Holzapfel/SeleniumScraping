import pycountry


t1 = pycountry.countries

dir(t1)

t2 = t1.get(alpha_2='DE')
type(t2)
import collections




dir(collections)

de_st = pycountry.subdivisions.get(code='DE-ST')

type(de_st)
country_obj = pycountry.countries.lookup("Germany")
type(country_obj)

pycountry.db.Country

pycountry.countries

dir(pycountry.countries)


t3 = {}
type(t3)
