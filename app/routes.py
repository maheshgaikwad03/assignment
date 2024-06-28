from flask import render_template, url_for, flash, redirect, request
from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm, RecipeForm
from app.models import User, Recipe
from flask_login import login_user, current_user, logout_user, login_required

@app.route("/")
@app.route("/dashboard")
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=True)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/recipe/new", methods=['GET', 'POST'])
@login_required
def new_recipe():
    form = RecipeForm()
    if form.validate_on_submit():
        recipe = Recipe(title=form.title.data, description=form.description.data,
                        ingredients=form.ingredients.data, instructions=form.instructions.data, author=current_user)
        db.session.add(recipe)
        db.session.commit()
        flash('Your recipe has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('recipe_form.html', title='New Recipe', form=form)

@app.route("/recipe/<int:recipe_id>")
def recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    return render_template('recipe_detail.html', title=recipe.title, recipe=recipe)

@app.route("/recipe/<int:recipe_id>/update", methods=['GET', 'POST'])
@login_required
def update_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    if recipe.author != current_user:
        abort(403)
    form = RecipeForm()
    if form.validate_on_submit():
        recipe.title = form.title.data
        recipe.description = form.description.data
        recipe.ingredients = form.ingredients.data
        recipe.instructions = form.instructions.data
        db.session.commit()
        flash('Your recipe has been updated!', 'success')
        return redirect(url_for('recipe', recipe_id=recipe.id))
    elif request.method == 'GET':
        form.title.data = recipe.title
        form.description.data = recipe.description
        form.ingredients.data = recipe.ingredients
        form.instructions.data = recipe.instructions
    return render_template('recipe_form.html', title='Update Recipe', form=form)

@app.route("/recipe/<int:recipe_id>/delete", methods=['POST'])
@login_required
def delete_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    if recipe.author != current_user:
        abort(403)
    db.session.delete(recipe)
    db.session.commit()
    flash('Your recipe has been deleted!', 'success')
    return redirect(url_for('home'))

@app.route("/")
@app.route("/home")
@login_required
def home():
    page = request.args.get('page', 1, type=int)
    pagination = Recipe.query.order_by(Recipe.date_posted.desc()).paginate(page=page, per_page=5)
    recipes = pagination.items
    return render_template('recipe_list.html', recipes=recipes, pagination=pagination)
