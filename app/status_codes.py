HTTP_200_OK = 200
HTTP_201_CREATED = 201  # Data has been successfully returned
HTTP_202_ACCEPTED = 202  # Wen the new user hasbeen succefully created
HTTP_400_BAD_REQUEST = 400  # When invalid information has been entered ie short password..
# This is returned when you have not entered all fields.
HTTP_401_UNAUTHORIZED = 401
HTTP_404_NOT_FOUND = 404  # The URL is incorrect or the file/page has been removed.
HTTP_500_INTERNAL_SERVER_ERROR = 500  # If there are any mistakes in the creation process
HTTP_409_CONFLICT = 409  # When anything entered has already been used
HTTP_403_FORBBIDEN = 403  # Invalid authentication credentials
HTTP_409_NOT_CONFLICT = 409  # When anything entered has already been used