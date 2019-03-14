# ISO 281 Bearing Life Calculations

This notebook implements a fatigue life estimation approach for ball and roller bearings using the ISO 281 approach, adopted for use for bearings in oscillatory applications such as wind and tidal turbine pitch systems according to NREL Wind Turbine Design Guideline 03: Yaw and Pitch Bearing Life.

![image](https://user-images.githubusercontent.com/25690525/54380499-8c4c9500-4683-11e9-8c0d-528f0ed48c2d.png)

## Program Description and Structure
The program runs assuming loading calculations have already been carried out either via simulation or from sensor readings on the turbine. An excel file for each load case must be created and hava an associated duty cycle. 

##### Load case data requirements (from simulations or sensor readings):
Blade root forces and bending moments (Fxy, Fz, My)
Pitch angle displacement
Timesteps

![image](https://user-images.githubusercontent.com/25690525/54380602-c6b63200-4683-11e9-8d8c-0b45f0eb7df1.png)


#### The process for the program:
1) Load the loading data
2) Create brg_design object using design parameters
3) Create load_case_comb object  - to combine load cases from each tidal profile
4) Create tidal_profile_comb object - to combine all tidal profiles with duty cycle information
5) Create life_calcs object to get pitch system bearing lifetime estimation



## How users get started



## Maintenance and Support
Where users can help
Who maintains and contributes

## Copyright

MIT License

Copyright (c) 2019 Fraser Ewing

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
