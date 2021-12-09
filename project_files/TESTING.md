## **TESTING**

### Table of contents
1. [W3C Validation](#Validation)
1. [User Stories Testing](#User-Stories-Testing)
1. [Responsive Design Test](#Site-Responsive-design-test)
1. [CRUD Test](#CRUD)
1. [Testing Forms and validation](Testing-Forms-and-validation)
1. [Future Testing](#Future-Testing)
1. [Bugs](#Bugs)
1. [Solved issues or bugs](#Solved-issues-or-bugs)
1. [Back to Readme.md](../README.md)

### **Validation**
  The W3C Markup Validator and W3C CSS Validator Services were used to validate every page of the project to ensure there were no syntax errors in the project.

- W3C Markup Validator
  - [Index Page](../project_files/validation/index.PNG)

- W3C CSS Validation
- PEP8 requirements
- Jshint


# [&#8686;](#Testing)
[Back to Readme.md](../README.md)
## ***UX*** 
### **User Stories Testing**
#### User goals

#### As Registered user

#### As an Administrator

#### Site owner goals


# [&#8686;](#Testing)
[Back to Readme.md](../README.md)

### Site Responsive design test
The Website is fully responsive and will cover most of the devices (screen sizes) and resolutions with minimum width of 330px.

Below i have attached testing gif video for each page tested.
- Index Page [GIF]()


# [&#8686;](#Testing)
[Back to Readme.md](../README.md)

### CRUD 
(create, read, update, and delete) Test
- Create

- Read

- Update

- Delete


### Testing Forms and validation

### **Future Testing**
I have tested the app on a variety of browsers such as  Chrome, Opera, Microsoft Edge, and Firefox desktop version browsers and Huawei p30 Pro chrome and android browser.

I have used Chrome DevTools to Test a variety of devices such as Desktop, Laptop, iPhone7, iPhone 8 & iPhone X for responsive design.

Friends and family members helped point out any bugs or issues.

# [&#8686;](#Testing)
[Back to Readme.md](../README.md)
### **Bugs**

# [&#8686;](#Testing)
[Back to Readme.md](../README.md)
### **Solved issues or bugs**
- If cart is empty return user back to previose page but if previose page was cart raised key error.
 

```python
# To solve this i have used return two addresses for each scenario 
# if previos url was cart redirect to shopping else return previos url.
    cart = request.session.get('cart', {})
    url_back = HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    if url_back != None:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect(reverse('shop'))
```

- fixed cart after removeing items and then going back using back button and trying to remove the same item again rised key error.


```python
#  I have added it check in cart views cart function if cart session has items in or not.
  if request.POST and cart:
```

# [&#8686;](#Testing)
[Back to Readme.md](../README.md)