def old_create_object(request, object_class):
    """Process POST form for generic Object 

    if the object doesn't exist, creates the object
    """
    if request.method == "POST":
        # Concatinate object class to get correct form name
        form_name = "Create_%s" % object_class
        # Grab class for db creation and initialize with POST info
        post_form = getattr(forms, form_name)(request.POST)
        if post_form.is_valid():
            # Sort form variables into dicts of init variables and foreign keys
            init_dict = {}
            fk_dict = {}
            # iterate through a sanatized dict of inputs
            for form_field, form_value in post_form.cleaned_data.iteritems():
                if '_fk' in form_field:
                    fk_dict.update({form_field:form_value})
                else:
                    init_dict.update({form_field:form_value})
            try:
                # Grab Class for db creation
                initializer = getattr(models, object_class)
                # Create new_object
                new_object = initializer(**init_dict)
            except Exception as e:
                print e 
                new_object = None

            # Save object before adding many-to-many relation
            if new_object is not None:
                new_object.save()

            # Iterate through foreign keys and add them to the 
            for fk in fk_dict:
                print blah

            user = helpers.Retrieve_Object("User", request.session['user_name'])

            try:
                new_object.users.add(user)
            except Exception as e:
                print e 
                new_object = None

            if new_object is not None:
                new_object.save()

    return HttpResponseRedirect('/clouds')

