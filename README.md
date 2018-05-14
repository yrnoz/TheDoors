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



some details:

![image](https://user-images.githubusercontent.com/33027226/39673666-1fd6aa12-5149-11e8-84b3-ed60e49794a1.png)


users ---> friends:  every user have friends in the friends table

users ---> facilities: every user is a worker in a company, so the user have a list of facilities of the company

users ---> orders: every user can to create an order, so the orders of this users saved in this table

users ---> schedules: every order translated into user schedules at last, so this table save the schedule of every user.

rooms <---> schedules: if we want to know the schedule of this rooms, when it full or empty etc

rooms <---> facilities: every room is part of facility.

schedules <---> order: every meeting on the schedule table is related to order object that match it



![image](https://user-images.githubusercontent.com/33027226/39562434-4acdf0a0-4eb4-11e8-9140-567f0bcb5fd0.png)

add table for facilities
