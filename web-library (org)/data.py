student = {
    'keys' : ["USER ID", "PASSWORD","FULL NAME","DEPARTMENT","MOBILE NUMBER","FINE"]
}
admin = {
    'keys' : ["USER ID","ADMIN NAME", "PASSWORD",]
}
book = {
    'keys' : ["BOOK CODE","BOOK NAME", "AUTHOR NAME","EDITION","DEPARTMENT","NO OF BOOKS",]
}
issue = {
    'keys' : ["ISSUE ID","USER ID","BOOK ID","ISSUE DATE","RETURN DATE"]
}
history = {
    'keys' : ["ISSUE_ID","USER_ID","BOOK_ID","ISSUE_DATE","RETURN_DATE","STATUS","FINE"]
}
user_details = {
    'keys' : ["ISSUE_ID","USER_ID","BOOK_ID","ISSUE_DATE","RETURN_DATE","STATUS"]
}

tables = {
    'student' : student,
    'admin' : admin,
    'book' :book,
    'issue':issue,
    'history':history,
}
