# TheDoors
[![codecov](https://codecov.io/gh/TechnionYearlyProject/TheDoors/branch/master/graph/badge.svg)](https://codecov.io/gh/TechnionYearlyProject/TheDoors)

[![Build Status](https://travis-ci.org/TechnionYearlyProject/TheDoors.svg?branch=master)](https://travis-ci.org/TechnionYearlyProject/TheDoors)

Solving the Door Permissions Problem



instructions for the working with html pages:

* change any href/src in the html page to function url_for:
<script src="some path for the code\image\etc"></script> 
-----------------------chnage to ----------------->
<script src="{{ url_for('static', filename=path for what you need') }}"></script>

* if we need a link between 2 pages:
                                href = Simulation. html
                        -------------chnage to --------------->
                            href="url_for('route_simulation')"
were 'route_simulation' is a function in main.py that return the Simulation.html page

* 'static' - this is directory that contain enything that html files needs

* Give a name to every input field ---->  <input type="email" name="email"  value={{ email }} required>

the 'required' keyword make this field to be required
and this part 'value={{ email }}' give a default value to this field
the 'email' is sent from the backend (specific in main.py in login_user method)
