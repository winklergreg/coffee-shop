/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'dev-jmn05h4b.us', // the auth0 domain prefix
    audience: 'coffee-api', // the audience set for the auth0 app
    clientId: 'X9sJ6bU3UeJIKNY8Wi3Q6GTSvpRryjnD', // the client id generated for the auth0 app
    callbackURL: 'http://127.0.0.1:8145', // the base url of the running ionic application. 
  }
};
