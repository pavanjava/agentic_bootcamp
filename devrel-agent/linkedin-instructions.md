# LinkedIn App Setup for OAuth Authentication

## Steps to Create LinkedIn App and Obtain Client ID and Secret

1. **Go to the LinkedIn Developers Portal**
    - Navigate to the [LinkedIn Developer Portal](https://www.linkedin.com/developers/).
    - If you don't have an account, create one using your LinkedIn credentials.

2. **Create a New Application**
    - Click on **"Create App"** at the top right corner of the page.
    - Fill in the necessary details:
        - **App Name**: Choose a name for your app.
        - **LinkedIn Page**: Optional, but link a page if applicable.
        - **App Description**: Briefly describe the purpose of the app.
        - **App Logo**: Upload a logo (square logo recommended).
        - **Business Information**: Enter details about your business.
    - Agree to LinkedIn’s **Terms of Use** and **Privacy Policy**.

3. **Obtain Client ID and Client Secret**
    - Once the app is created, navigate to the **Auth** tab in your app settings.
    - Copy the **Client ID** and **Client Secret**.
        - These will be required for OAuth authentication.

4. **Set the Redirect URL**
    - In the **Auth** tab, you will also need to define the redirect URLs.
        - **Redirect URLs** are the locations where LinkedIn will send users after they authorize your app.
        - Example: `https://yourdomain.com/linkedin/callback`
    - Add the authorized redirect URL for your application.

5. **Set OAuth Scopes**
    - Under the **OAuth 2.0 Scopes** section, select the appropriate scopes for your application. Some common scopes are:
        - `r_liteprofile` (Basic profile information)
        - `r_emailaddress` (Email address)
        - `w_member_social` (Post updates on behalf of the member)
    - Make sure to choose the right scopes based on your app's requirements.

6. **Save Changes**
    - After setting up the client ID, client secret, scopes, and redirect URL, click **Save** to update your app settings.


