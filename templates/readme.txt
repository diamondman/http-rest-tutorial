These files are called templates. They are mostly html with weird extra syntax in them. Stuff in {{ }} will directly print python variables passed to render_template (like entry=plant) into the html.
Example
<a href="/plant/{{entry.id}}">
will become after render_template is called in python
<a href="/plant/5">
Or whatever the id of the entry is.

Some sections will have bits of code surrounded by {%  %}. That is for doing more interesting things in code, like including other template files, or making for loops in the template.
Including other files lets us not have to type the header and footer in every damn file. And for loops let us write how to print an entry in a table once and then output that html for every entry in an array.

The templating system should be using Jinja2, or something compatable with it.
Jinja2 is described here: http://jinja.pocoo.org/docs/dev/
