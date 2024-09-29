import logging
import time

import click
from celery import shared_task
from extensions.ext_mail import mail
from flask import render_template


@shared_task(queue="mail")
def send_deletion_success_task(language, to):
    """Send email to user regarding account deletion.

    Args:
        log (AccountDeletionLog): Account deletion log object
    """
    if not mail.is_inited():
        return

    logging.info(
        click.style(f"Start send account deletion success email to {to}", fg="green")
    )
    start_at = time.perf_counter()

    try:
        if language == "zh-Hans":
            html_content = render_template(
                "delete_account_mail_template_zh-CN.html",
                to=to,
                # TODO: Add more template variables
            )
            mail.send(to=to, subject="Dify 账户删除成功", html=html_content)
        else:
            html_content = render_template(
                "delete_account_mail_template_en-US.html",
                to=to,
                # TODO: Add more template variables
            )
            mail.send(to=to, subject="Dify Account Deleted", html=html_content)

        end_at = time.perf_counter()
        logging.info(
            click.style(
                "Send account deletion success email to {} succeeded: latency: {}".format(to, end_at - start_at), fg="green"
            )
        )
    except Exception:
        logging.exception("Send account deletion success email to {} failed".format(to))
