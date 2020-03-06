#!/bin/bash

users="matheus.mytec filipe.mytec lucas.mytec railander.mytec thailan.mytec andre.mytec lucast.mytec"

for user in $users
do
	aws iam create-user --user-name "$user" --profile $AWS_PROFILE
	aws iam create-login-profile --user-name "$user" --password Mytec@2020 --password-reset-required --profile $AWS_PROFILE
	aws iam add-user-to-group --user-name "$user" --group-name admin --profile $AWS_PROFILE
done
