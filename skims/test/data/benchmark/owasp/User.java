public class User {
    public String name;
    private String lastName;
    private String userId;

    public User(String name) {
        /*
         * there must be a reference to the current instance, that instance must be
         * passed to the setName function
         */
        this.setName(name);
    }

    public User(String name, String lastName) {
        /*
         * it must be recognized as a constructor with the signature User_2, the current
         * instance must be passed to the setName function, but it must also be modified
         * by the declaration
         */
        setName(name);
        this.lastName = lastName;
    }

    public User(String name, String lastName, String Id) {
        setName(name);
        this.lastName = lastName;
        userId = Id;
    }

    public String getName() {
        // it must to return the value of the field referring to the current instance
        return name;
    }

    public void setName(String name) {
        // this should modify the field referencing the current instance
        this.name = name;
    }

    public String getUserId() {
        int someNumber = 13;
        String Id = this.userId;
        return Id;
    }

    public void setUserId(String userId) {
        this.userId = userId;
    }

    public void setLastName(String lastName) {
        this.lastName = lastName;
    }

}
