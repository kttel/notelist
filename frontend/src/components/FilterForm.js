const FilterForm = ({query, handleFiltering, getNotes}) => {
  const handleSubmit = (e) => {
    e.preventDefault();
    getNotes();
  }

  return (
    <div className="filter-block">
        <form onSubmit={e => handleSubmit(e)}>
            <input placeholder="Search by keywords or category"
                value={query}
                onChange={e => handleFiltering(e.target.value)} />
        </form>
    </div>
  );
};

export default FilterForm;