import 'dart:developer';

import 'package:flutter/foundation.dart';

import 'package:flutter/material.dart';
import 'package:manager/content.dart';
import 'package:manager/services/auth.dart';
import 'package:manager/services/auth.exceptions.dart';

class LoginWidget extends StatefulWidget {
  const LoginWidget({Key? key}) : super(key: key);

  @override
  State<LoginWidget> createState() => _LoginWidgetState();
}

class _LoginWidgetState extends State<LoginWidget> {
  late TextEditingController _emailController;
  late TextEditingController _passwordController;

  final AuthService _auth = AuthService();

  final _formKey = GlobalKey<FormState>();

  String _message = "";

  @override
  void initState() {
    super.initState();

    _emailController = TextEditingController();
    _passwordController = TextEditingController();

    if (kDebugMode) {
      setState(() {
        _emailController.text = 'admin@test.com';
        _passwordController.text = '1234';
      });
    }
  }

  @override
  void dispose() {
    _emailController.dispose();
    _passwordController.dispose();
    super.dispose();
  }

  void signIn() async {
    authenticate().then((success) {
      if (success) {
        setState(() {
          _message = ""; // remove old messages
        });

        Navigator.push(
          context,
          MaterialPageRoute(builder: (context) => const ContentWidget()),
        );
      }
    });
  }

  Future<bool> authenticate() async {
    final token = await _auth
        .getAPIToken(
      email: _emailController.text,
      password: _passwordController.text,
    )
        .catchError(
      (error) {
        log("Server unreachable");
        setState(() {
          _message = "Could not reach authentication server";
        });
        return "";
      },
      test: (error) => error is ServerUnreachableException,
    ).catchError(
      (error) {
        log("Invalid credentials");
        setState(() {
          _message = "Email and password is incorrect";
        });
        return "";
      },
      test: (error) => error is AuthenticationException,
    ).catchError((error) {
      log("Unknown error: ${error.toString()}");
      return "";
    });

    if (token == "") return false;

    // get oauth 2 token
    await _auth
        .getOAuth2Token(
      email: _emailController.text,
      password: _passwordController.text,
    )
        .catchError(
      (error) {
        setState(() {
          _message = error.toString();
        });
      },
      test: (error) => error is AuthenticationException,
    );

    await _auth.getUserFromToken();

    await _auth.getUserRoles();
    await _auth.getRoles();

    return true;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Container(
          width: 500,
          padding: const EdgeInsets.all(10),
          child: Form(
            key: _formKey,
            child: Column(
              mainAxisAlignment: MainAxisAlignment.start,
              children: [
                const SizedBox(height: 30),
                const Text(
                  'Sign in',
                  style: TextStyle(
                    fontWeight: FontWeight.bold,
                    fontSize: 30,
                  ),
                ),
                const SizedBox(height: 20),
                TextFormField(
                  controller: _emailController,
                  validator: (String? value) {
                    if (value != null && value.isEmpty) {
                      return "This field is required";
                    }
                    return null;
                  },
                  decoration: const InputDecoration(
                    border: OutlineInputBorder(),
                    labelText: "Email",
                  ),
                ),
                const SizedBox(height: 20),
                TextFormField(
                  controller: _passwordController,
                  validator: (String? value) {
                    if (value != null && value.isEmpty) {
                      return "This field is required";
                    }
                    return null;
                  },
                  decoration: const InputDecoration(
                    border: OutlineInputBorder(),
                    labelText: "Password",
                  ),
                  obscureText: true,
                ),
                const SizedBox(height: 20),
                Visibility(
                  visible: _message.isNotEmpty,
                  child: Row(
                    children: [
                      Expanded(
                        child: Card(
                          color: Colors.amber,
                          child: Padding(
                            padding: const EdgeInsets.all(8.0),
                            child: Text(_message),
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
                ElevatedButton(
                  onPressed: () {
                    if (_formKey.currentState!.validate()) {
                      signIn();
                    }
                  },
                  child: const Text("Sign in"),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
