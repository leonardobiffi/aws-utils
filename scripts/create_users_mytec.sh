#!/bin/bash

users="matheus.mytec filipe.mytec lucas.mytec railander.mytec thailan.mytec andre.mytec"

for user in $users
do
	aws iam create-user --user-name "$user"
	aws iam create-login-profile --user-name "$user" --password Mytec@2020 --password-reset-required
	aws iam add-user-to-group --user-name "$user" --group-name admin
done