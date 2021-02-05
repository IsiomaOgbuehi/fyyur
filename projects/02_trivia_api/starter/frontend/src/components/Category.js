import React, { Component } from 'react'

class Category extends Component{
    state = {
        category: '',
    }

    setCategory = (event) => {
        event.preventDefault();
        this.props.addCategory(this.state.category)
    }

    handleInputChange = () => {
        this.setState({
            category: this.cat.value
        })
    }

    render() {
        return (
            <form onSubmit={this.setCategory} id="add-category">
                <br />
                <h3> Add Category </h3>
                <input
                    placeholder="Add Category"
                    ref={input => this.cat = input}
                    onChange={this.handleInputChange}
                />
                <input type="submit" value="Add" className="button"/>
            </form>
        )
    }
}

export default  Category