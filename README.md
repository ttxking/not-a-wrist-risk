# Smart Wristband

### Technology used
<img alt="Python" src="https://img.shields.io/badge/python%20-%2314354C.svg?&style=for-the-badge&logo=python&logoColor=white"/> <img alt="Flask" src="https://img.shields.io/badge/flask%20-%23000.svg?&style=for-the-badge&logo=flask&logoColor=white"/>

### Description

This is the backend repository for smartwristband project which is the paart of exceed17 camp

### API

* GET
    * /get_movement or /get_movement/?movement_id={value}
        * return value of the movement
    ``` 
        {           
            "movement_id": int,
            "fast_movement": int(1,0),  # 1 means exists, 0 vice versa
            "no_movement": int(1,0)
        } 
    ```
    * /get_light or /get_light?light_id={value}
        * return value of the light margin between devices and the room
    ```
        {
            "light_id": int,
            "light_sensitivity": int # difference between two LDR
        }

    ```
    * /get_location_status
        * return value of finding location finding status
    ```
        {
            "finding_status": int(1,0) # 1 means finding, 0 vice versa
        }

    ```
    * /information or /information?user_id={value}
        * return statistics summary of the users
    ```
        {
            "user_id": ele["user_id"],
            "movement_status": ele["movement_status"],  # too little ,too much
            "light_status": ele["light_status"],  # too dark, too bright
            "movement_time": ele["movement_time"],  # total movement time
            "calories": ele["calories"] # total calories burnt
        }
    ```
* POST
    * /create_user
        * create a user for keeping record, the **INPUT** format is 
    ```
        {
            "user_id": int # the rest will be created with default value
        }
    ```
    * /create_movement
        * create movement recorded by the gyro, the **INPUT** format is
    ```
        {
            "movement_id": int,
            "fast_movement": int(1,0),  # 1 means exists, 0 vice versa
            "no_movement": int(1,0)
        }
    ```
    * /create_light
        * create light sensitivity recored by the LDR, the **INPUT** format is
    ```
        {
            "light_id": int,
            "light_sensitivity": int # difference between two LDR 
        }
    ```
* PUT 
    * /cal_movement?user_id={value}
        * update movement status of specific user

    * /cal_light?user_id={value}
        * update light status of specific user
 
    * /cal_calories_and_time?user_id={value}
        * update calories and total movement time of specific user
    
    * /update_location_status
        * update finding status 0 if the user is not using finding mode, 1 vice versa.  the **INPUT** format is
    ```
        {
           "finding_status": int(0,1)
        }
    ```
    * /reset_info?user_id={value}
        * reset user info after 1 day

### ROUTING IP
    158.108.182.16:500014  # PS. Port may changed due to traffic please contact me
