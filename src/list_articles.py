import click
import json as jsonPkg
from utils import fetch, files


@click.command()
@click.option('--export', is_flag=True, default=False)
@click.option('--json', is_flag=True, default=False)
@click.option('--csv', is_flag=True, default=False)
@click.option('--limit', type=int, default=5)
@click.option('--page', type=int, default=1)
@click.pass_context
def list_articles(ctx, limit, export, json, csv, page):
    """This is a command that returns a list of articles to
    Arguments:
        article {[string or id]} -- [unique identifier for the article]
    """
    response = fetch.get('articles?page_size={}&page={}'.format(limit, page))
    articles = response.json().get('articles', {})
    click.echo(jsonPkg.dumps(articles, indent=4))
    if export:
        filename = "all_articles"
        if json:
            files.export_to_json(filename=filename, data=articles)
        if csv:
            files.export_to_csv(filename=filename, data=articles)
    next_q = click.prompt(
        "Use [n] to go next page or [q] to exit", default='n')
    if next_q.lower() == 'n':
        ctx.invoke(list_articles,
                   limit=limit, export=False, page=page+1)
