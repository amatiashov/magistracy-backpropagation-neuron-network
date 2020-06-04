FROM python:3.6.3-onbuild

EXPOSE 8080

ENTRYPOINT ["./run.sh"]
