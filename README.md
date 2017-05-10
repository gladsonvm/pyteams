# pyteams

Pyteams is a light weight team management application written in python. Using Pyteams different teams
and team members can communicate with each other and keep in sync. Pyteams provide backend features to
facilitate team management.

### Concepts
 * Team

    * Teams are the basic concept on which pyteams are built upon. A team can have any number
    of members or a finite number of members as specified by a team manager. A team object is
    uniquely identified by its name and department `unique_together = ('name', 'team_type',)`.

 * Tasks

    * A task is an assignment given to any team member which have a starting time and an ETA.
     Task can be assigned to team members by a manager or by the same team member(self assigned task).

 * Activities

    * Activities are used to keep track of tasks by watching all types of engagements with the
    corresponding task. Activities can be sub tasks also. Activities can also have comments and
    replies linked with them. These comments and replies can form a thread.

### order of calling

 * Abbreviations
    * rq: request
    * hn: handler
    * mtd: method_name
    * val: value
    * resp: response


```
                                    3. resp/data
                            ______________________________
                           |                              |
                           |                              |
             1.            v           2.                 |
frontend --------> Django Views.py ---------> decorator ---
  ^    rq, hn, mtd      |          rq, args,
  |    val              |             kwargs
  |                     |
  |_____________________|
     4.   response/data

```

frontend will query pyteams backend with request and data. Request and data will be passed to backend
through urls.

 * url end point format
    * /handler/method/id
        * id can be replaced with `all` to get all objects the corresponds to a given handler
        and authenticated user. However all is not applicable if copious amount of objects are
        returned by orm query. In that case recently updated 20 objects will be returned.

        eg: http://localhost:8000/team/get/1, http://localhost:8000/team/get/all

* sample request
    * url: http://localhost:8000/team/get/1

        response:
```
                {
                    "objects": [
                                    {
                                          "created_by_id": "2",
                                          "description": "testing guardian perms",
                                          "name": "guards",
                                          "team_type": "management",
                                          "updated_on": "2017-05-07 07:46:44.591273+00:00",
                                          "created_on": "2017-04-30 07:05:29.074708+00:00",
                                          "id": "1"
                                        }
                                    ],
                    "meta": {
                        "total_objects": 1,
                        "resource_uri": "/team/get/1/?pretty"
                      }
                }
```