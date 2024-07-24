from django.db import models

class UserDetails(models.Model):
    usrEmail = models.CharField(max_length=150, primary_key=True)
    files_list = models.JSONField(default=list)  #can be changed to ManyToMany

    def __str__(self):
        return self.usrEmail


class Doctors(models.Model):
    doc_uname = models.CharField(primary_key=True, default="default_name", max_length=150)
    doc_name = models.CharField(max_length=150)
    doc_qualifications = models.CharField(max_length=150)
    verified_list = models.JSONField(default=list)

    def __str__(self):
        return str(self.doc_uname) 

class FileDetails(models.Model):
    file_name = models.CharField(primary_key=True, default="default_name", editable=False, max_length=150)
    json_image_data = models.JSONField(default=dict)
    str_image_text = models.TextField(default='No Data Found!!')
    data_from_llm = models.JSONField(default=dict)
    file_url = models.CharField(max_length=150, default='/assets/image_not_found.svg')
    upload_date = models.DateTimeField(auto_now=True)
    
    isVerified = models.IntegerField(default=0)  #0: not verifed, 1:verified all good, 2: verified with comments
    verification_doc = models.ForeignKey(Doctors, on_delete=models.SET_NULL, null=True, blank=True)
    verification_date =  models.DateTimeField(null=True, blank=True, default=None)
    verification_comment = models.CharField(max_length=800, default='', null=True, blank=True)

    def __str__(self):
        return str(self.file_name)
