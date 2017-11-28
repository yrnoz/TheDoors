class Employee:
     def _init_ (self ,  id, name, access_permission):
         self.id = id
         self.name = name
         self.access_permission = access_permission

     def get_access_permission(self):
         return self.access_permission