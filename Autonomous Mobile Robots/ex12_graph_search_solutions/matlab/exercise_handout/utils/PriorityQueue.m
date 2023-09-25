classdef PriorityQueue < handle
    %   Very lazy implementation of a priority queue 
    
    properties
        pq
        n_cols
        n_rows
    end
    
    methods
        function obj = PriorityQueue(initial_array, varargin)
            %Initial array should be n x m, first column is priority,
            % second column is id, other columns can be anything 
            % (for graph search best parent id)
            % Optional argument to set initial size (make it as big as
            % needed to allow preallocation, but keep track of num elements
            % with the n_rows variable)
            if nargin >= 2
                max_size = varargin{1};
            else
                max_size = size(initial_array, 1);
            end                
            
            obj.n_cols = size(initial_array, 2);
            obj.n_rows = size(initial_array, 1);
            obj.pq = zeros(max_size, obj.n_cols);
            obj.pq(1:obj.n_rows, :) = sortrows(initial_array,1);            
        end
        
        function push(obj, new_element)
            % Push new element
            %   We will resolve duplicates by replacing if lower cost
            assert(all(size(new_element) == [1, obj.n_cols]), 'New element is incorrect size, must be [1x%d]', obj.n_cols)
            
            % Check if it's already in the queue
            % This is not an efficient implementation, just a clear one
            old_pos = find(obj.pq(1:obj.n_rows, 2)==new_element(2), 1, 'first');
            
            if isempty(old_pos)
                % Not in current queue
                new_pos = find(obj.pq(1:obj.n_rows, 1) > new_element(1), 1, 'first');
                if isempty(new_pos)
                    new_pos = obj.n_rows+1;
                end
                
                % Shift down old values with higher cost
                obj.pq((new_pos+1):(obj.n_rows+1), :) = obj.pq(new_pos:obj.n_rows, :);
                obj.pq(new_pos, :) = new_element;
                obj.n_rows = obj.n_rows+1;
            elseif new_element(1) < obj.pq(old_pos,1)
                % If it has a lower cost than the old one
                new_pos = find(obj.pq(1:obj.n_rows, 1) > new_element(1), 1, 'first');
                
                % We shift everything between new pos and old pos down
                % (overwriting existing element) and insert the new one
                obj.pq((new_pos+1):old_pos, :) = obj.pq(new_pos:(old_pos-1), :);
                obj.pq(new_pos, :) = new_element;
            
            end
            % If it was already there with a better cost we don't do
            % anything
        end
        
        function element = pop(obj)
            element = obj.pq(1,:);
            obj.pq(1:obj.n_rows-1,:) = obj.pq(2:obj.n_rows,:);
            obj.n_rows = obj.n_rows-1;
        end       
        
    end
end

