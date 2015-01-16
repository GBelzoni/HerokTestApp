window.fbAsyncInit = function() {
  
  var app_domain = 'localhost:9003'
  var app_id = '714612301882745' //pc local dev
  // var app_id = '565857103493139' //ihub dev
  
   
  FB.init({
    appId      : app_id, // App ID
    channelUrl : '//' + app_domain + '/channel.html', // Channel File
    status     : true, // check login status
    cookie     : true, // enable cookies to allow the server to access the session
    xfbml      : true  // parse XFBML
  });

  // Here we subscribe to the auth.authResponseChange JavaScript event. This event is fired
  // for any authentication related change, such as login, logout or session refresh. This means that
  // whenever someone who was previously logged out tries to log in again, the correct case below 
  // will be handled. 
  FB.Event.subscribe('auth.authResponseChange', function(response) {
    // Here we specify what we do with the response anytime this event occurs. 
    var token;
    if (response.status === 'connected') {
      // The response object is returned with a status field that lets the app know the current
      // login status of the person. In this case, we're handling the situation where they 
      // have logged in to the app.
      
      token = response.authResponse.accessToken;
      // alert( 'got token');
      testAPI();
    } else if (response.status === 'not_authorized') {
      // In this case, the person is logged into Facebook, but not into the app, so we call
      // FB.login() to prompt them to do so. 
      // In real-life usage, you wouldn't want to immediately prompt someone to login 
      // like this, for two reasons:
      // (1) JavaScript created popup windows are blocked by most browsers unless they 
      // result from direct interaction from people using the app (such as a mouse click)
      // (2) it is a bad experience to be continually prompted to login upon page load.
      FB.login();
    } else {
      // In this case, the person is not logged into Facebook, so we call the login() 
      // function to prompt them to do so. Note that at this stage there is no indication
      // of whether they are logged into the app. If they aren't then they'll see the Login
      // dialog right after they log in to Facebook. 
      // The same caveats as above apply to the FB.login() call here.
      FB.login();
    }
    
    
    //Button handlers
    var domain_url ='http://' + app_domain  

    //Button handler - short AT
    var stor_url = domain_url + '/receive_simple/';
    var get_short_AT_str = stor_url + token;
    $(document).ready(function(){
      $("#get_short_AT").click(function(){
        $("#div1").load(get_short_AT_str);
      });
    }); 
    
    //Button handler - long AT
    $(document).ready(function(){
      $("#get_long_AT").click(function(){
        $("#div2").load(domain_url + '/get_long_AT');
      });
    }); 
    
  });
};

// Load the SDK asynchronously 
(function(d){
var js, id = 'facebook-jssdk', ref = d.getElementsByTagName('script')[0];
if (d.getElementById(id)) {return;}
js = d.createElement('script'); js.id = id; js.async = true;
js.src = "//connect.facebook.net/en_US/all.js";
ref.parentNode.insertBefore(js, ref);
}(document));

//rHere we run a very simple test of the Graph API after login is successful. 
// This testAPI() function is only called in those cases. 
function testAPI() {
  console.log('Welcome!  Fetching your information.... ');
  FB.api('/me', function(response) {
    console.log('Good to see you, ' + response.name + '.');
  });
}




