This function takes a `dict`,
`keys` being `str`,
`values` being `int` where unmixed,
`str` where mixed.

The old PHP code set those `values` as `int`,
so I assumed that the current form would do so.

Here is an example of that which I assumed `data` to be:

data = {
    'bedrooms':1,
    'bath_total':1,
    'sqft':3000,
    'avm':175000,
    'avm_low':100000,
    'avm_high':300000,
    'street':'123 Somestreet Ln.',
    'city':'Townsville',
    'state':'Florida',
    'zip':69666
}

The function tests whether important fields are filled.
If there's a 'fieldless' email template to be sent in such case,
let me know, and I shall add logic to return that otherwise.

Dollar signs on `data.avm` ...etc.
are not to be included in templates;
they are added—fails if `ints` are initially `strs`.

In templates,
the `values` of `data` can be accessed by:
{{ data.something }}

Any HTML file should work, just replace it in line #30:
    `template = j2.Template(open('somefile.html').read())`